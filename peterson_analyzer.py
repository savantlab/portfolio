#!/usr/bin/env python3
"""
Automated Peterson Podcast Analyzer

This script runs automated analysis on Peterson podcast transcripts:
- Fetches all episodes from Flask API
- Runs predefined analysis queries through Ollama
- Generates structured reports
- Saves results to output directory

Designed to run in Docker with fresh Ollama instance each time.
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class PetersonAnalyzer:
    def __init__(self, flask_url, ollama_url, model="gemma3:latest", output_dir="/output"):
        self.flask_url = flask_url
        self.ollama_url = ollama_url
        self.model = model
        self.output_dir = output_dir
        self.podcasts = None
        
        # Load API token
        self.api_token = os.getenv('API_TOKEN')
        self.headers = {'Content-Type': 'application/json'}
        if self.api_token:
            self.headers['Authorization'] = f'Bearer {self.api_token}'
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
    
    def wait_for_ollama(self, timeout=300):
        """Wait for Ollama to be ready"""
        print("⏳ Waiting for Ollama to be ready...")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
                if response.status_code == 200:
                    print("✓ Ollama is ready")
                    return True
            except:
                pass
            time.sleep(5)
        
        print("❌ Timeout waiting for Ollama")
        return False
    
    def pull_model(self):
        """Pull the Ollama model if not available"""
        print(f"📥 Pulling model: {self.model}")
        try:
            response = requests.post(
                f"{self.ollama_url}/api/pull",
                json={"name": self.model},
                stream=True,
                timeout=600
            )
            
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    status = data.get('status', '')
                    if 'pulling' in status.lower():
                        print(f"  {status}")
            
            print(f"✓ Model {self.model} ready")
            return True
        except Exception as e:
            print(f"❌ Error pulling model: {e}")
            return False
    
    def load_podcasts(self):
        """Load podcast data from Flask API"""
        print(f"📡 Fetching podcasts from {self.flask_url}")
        try:
            response = requests.get(f"{self.flask_url}/api/podcasts", headers=self.headers)
            response.raise_for_status()
            self.podcasts = response.json()
            print(f"✓ Loaded {len(self.podcasts)} podcasts")
            return True
        except Exception as e:
            print(f"❌ Error loading podcasts: {e}")
            return False
    
    def query_ollama(self, prompt, system_prompt=None):
        """Query Ollama LLM"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=180
            )
            response.raise_for_status()
            result = response.json()
            return result.get('response', '')
        except Exception as e:
            return f"Error: {e}"
    
    def analyze_episode(self, podcast, analysis_type="themes"):
        """Analyze a single episode"""
        transcript = podcast.get('transcript', '')
        if not transcript:
            return {"error": "No transcript available"}
        
        # Limit transcript to avoid token limits
        transcript_excerpt = transcript[:4000]
        
        queries = {
            "themes": "Identify the main themes and topics discussed in this podcast excerpt. List 5-7 key themes.",
            "ideology": "Analyze the ideological framework presented in this excerpt. What worldview is being promoted?",
            "rhetoric": "What rhetorical strategies and persuasive techniques are used in this excerpt?",
            "terminology": "List the most frequently used specialized terms and concepts. What language patterns are notable?"
        }
        
        query = queries.get(analysis_type, queries["themes"])
        
        prompt = f"""Analyze this Jordan Peterson podcast transcript excerpt:

Guest: {podcast.get('guest', 'Unknown')}
Episode: {podcast['title']}

Transcript excerpt:
{transcript_excerpt}

Question: {query}

Provide a structured analysis."""

        system_prompt = "You are a research assistant analyzing podcast transcripts for academic research. Be factual and cite specific quotes."
        
        response = self.query_ollama(prompt, system_prompt)
        
        return {
            "podcast_id": podcast['id'],
            "title": podcast['title'],
            "guest": podcast.get('guest'),
            "analysis_type": analysis_type,
            "analysis": response,
            "transcript_length": len(transcript),
            "timestamp": datetime.now().isoformat()
        }
    
    def run_analysis(self):
        """Run complete analysis workflow"""
        print("\n" + "="*80)
        print("Peterson Podcast Automated Analysis")
        print("="*80)
        print(f"Model: {self.model}")
        print(f"Flask API: {self.flask_url}")
        print(f"Ollama API: {self.ollama_url}")
        print(f"Output: {self.output_dir}")
        print("="*80 + "\n")
        
        # 1. Wait for Ollama
        if not self.wait_for_ollama():
            return False
        
        # 2. Pull model
        if not self.pull_model():
            return False
        
        # 3. Load podcasts
        if not self.load_podcasts():
            return False
        
        # 4. Run analyses
        analysis_types = ["themes", "ideology", "rhetoric", "terminology"]
        all_results = []
        
        for podcast in self.podcasts:
            if not podcast.get('transcript'):
                print(f"\n⏭️  Skipping {podcast['id']} (no transcript)")
                continue
            
            print(f"\n📊 Analyzing: {podcast['title']}")
            
            for analysis_type in analysis_types:
                print(f"   - {analysis_type.capitalize()} analysis...")
                result = self.analyze_episode(podcast, analysis_type)
                all_results.append(result)
                
                # Small delay to avoid overwhelming Ollama
                time.sleep(2)
        
        # 5. Save results
        output_file = os.path.join(
            self.output_dir,
            f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        
        print(f"\n💾 Saving results to {output_file}")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        
        # 6. Generate summary report
        self.generate_summary_report(all_results)
        
        print("\n" + "="*80)
        print("✓ Analysis Complete")
        print("="*80)
        print(f"Total analyses: {len(all_results)}")
        print(f"Output: {output_file}")
        print("="*80)
        
        return True
    
    def generate_summary_report(self, results):
        """Generate human-readable summary report"""
        report_file = os.path.join(
            self.output_dir,
            f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# Peterson Podcast Analysis Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**Model:** {self.model}\n\n")
            f.write(f"**Episodes Analyzed:** {len(set(r['podcast_id'] for r in results))}\n\n")
            f.write("---\n\n")
            
            # Group by podcast
            by_podcast = {}
            for result in results:
                pid = result['podcast_id']
                if pid not in by_podcast:
                    by_podcast[pid] = []
                by_podcast[pid].append(result)
            
            for podcast_id, analyses in by_podcast.items():
                f.write(f"## {analyses[0]['title']}\n\n")
                f.write(f"**Guest:** {analyses[0].get('guest', 'Unknown')}\n\n")
                
                for analysis in analyses:
                    f.write(f"### {analysis['analysis_type'].capitalize()} Analysis\n\n")
                    f.write(f"{analysis['analysis']}\n\n")
                    f.write("---\n\n")
        
        print(f"✓ Summary report: {report_file}")


def main():
    flask_url = os.getenv('FLASK_URL', 'http://localhost:5001')
    ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
    model = os.getenv('OLLAMA_MODEL', 'gemma3:latest')
    output_dir = os.getenv('OUTPUT_DIR', './analysis_output')
    
    analyzer = PetersonAnalyzer(flask_url, ollama_url, model, output_dir)
    success = analyzer.run_analysis()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

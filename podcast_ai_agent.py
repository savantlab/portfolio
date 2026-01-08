#!/usr/bin/env python3
"""
Podcast AI Agent - Interactive discussion of podcast transcripts using Ollama.

This agent:
- Connects to your Flask API to retrieve podcast transcripts
- Uses Ollama LLM for natural language understanding
- Answers questions about podcast content
- Performs analysis and comparison across episodes

Usage:
    python podcast_ai_agent.py
    python podcast_ai_agent.py --model gemma3:latest
    python podcast_ai_agent.py --api-url http://localhost:5001
"""

import os
import sys
import json
import argparse
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class PodcastAIAgent:
    def __init__(self, flask_url="http://localhost:5001", ollama_url="http://localhost:11434", model="gemma3:latest"):
        self.flask_url = flask_url
        self.ollama_url = ollama_url
        self.model = model
        self.podcasts = None
        self.conversation_history = []
        
        # Load API token if available
        self.api_token = os.getenv('API_TOKEN')
        self.headers = {'Content-Type': 'application/json'}
        if self.api_token:
            self.headers['Authorization'] = f'Bearer {self.api_token}'
    
    def load_podcasts(self):
        """Load all podcast data from Flask API"""
        try:
            response = requests.get(f"{self.flask_url}/api/podcasts", headers=self.headers)
            response.raise_for_status()
            self.podcasts = response.json()
            print(f"✓ Loaded {len(self.podcasts)} podcasts")
            return True
        except Exception as e:
            print(f"❌ Error loading podcasts: {e}")
            return False
    
    def get_podcast_by_id(self, podcast_id):
        """Get specific podcast by ID"""
        if not self.podcasts:
            return None
        return next((p for p in self.podcasts if p['id'] == podcast_id), None)
    
    def search_podcasts(self, keyword):
        """Search for keyword in podcasts"""
        results = []
        for podcast in self.podcasts:
            transcript = podcast.get('transcript', '')
            if keyword.lower() in transcript.lower():
                count = transcript.lower().count(keyword.lower())
                results.append({
                    'podcast': podcast,
                    'count': count
                })
        return results
    
    def build_context(self, user_query):
        """Build context from podcast data for LLM"""
        context_parts = []
        
        # Always include available podcasts
        context_parts.append("Available podcasts:")
        for p in self.podcasts:
            guest = p.get('guest', 'Unknown')
            words = len(p.get('transcript', '').split())
            context_parts.append(f"- {p['id']}: {p['title']} (Guest: {guest}, {words:,} words)")
        
        context_parts.append("\nYou are an AI assistant helping analyze Jordan Peterson podcast transcripts.")
        context_parts.append("These transcripts are part of research into Peterson's rhetoric and ideological patterns.")
        
        return "\n".join(context_parts)
    
    def query_ollama(self, prompt, system_prompt=None):
        """Send query to Ollama and get response"""
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
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            return result.get('response', '')
        except Exception as e:
            return f"Error querying Ollama: {e}"
    
    def process_query(self, user_query):
        """Process user query with context and LLM"""
        
        # Check if query is asking about specific podcast
        query_lower = user_query.lower()
        
        # Build relevant context
        context = self.build_context(user_query)
        
        # Check if asking for specific podcast content
        for podcast in self.podcasts:
            if podcast['id'] in query_lower or podcast.get('guest', '').lower() in query_lower:
                # Include relevant transcript excerpt
                transcript = podcast.get('transcript', '')
                # Limit to first 3000 chars to avoid token limits
                context += f"\n\nExcerpt from {podcast['title']} transcript:\n{transcript[:3000]}..."
                break
        
        # Check if asking for search/comparison
        search_keywords = ['compare', 'difference', 'similar', 'both mention', 'across all']
        if any(keyword in query_lower for keyword in search_keywords):
            context += "\n\nNote: For comparative analysis, I can search across all transcripts."
        
        # Build full prompt
        full_prompt = f"{context}\n\nUser question: {user_query}\n\nAnswer:"
        
        # Query Ollama
        system_prompt = "You are a helpful research assistant analyzing podcast transcripts. Be concise and factual. Cite specific quotes when possible."
        response = self.query_ollama(full_prompt, system_prompt)
        
        return response
    
    def run_interactive(self):
        """Run interactive chat loop"""
        print("\n" + "="*80)
        print("🎙️  Podcast AI Agent - Interactive Mode")
        print("="*80)
        print(f"Model: {self.model}")
        print(f"Flask API: {self.flask_url}")
        print(f"Ollama API: {self.ollama_url}")
        print("\nCommands:")
        print("  - Type your question to discuss podcast content")
        print("  - 'list' - Show available podcasts")
        print("  - 'search <keyword>' - Search for keyword")
        print("  - 'load <podcast_id>' - Load specific podcast into context")
        print("  - 'quit' or 'exit' - Exit the agent")
        print("="*80 + "\n")
        
        # Load podcasts
        if not self.load_podcasts():
            print("Failed to load podcasts. Make sure Flask is running.")
            return
        
        current_context_podcast = None
        
        while True:
            try:
                user_input = input("\n🤔 You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye!")
                    break
                
                if user_input.lower() == 'list':
                    print("\n📻 Available podcasts:")
                    for p in self.podcasts:
                        words = len(p.get('transcript', '').split())
                        print(f"  - {p['id']}: {p['title']} ({words:,} words)")
                    continue
                
                if user_input.lower().startswith('search '):
                    keyword = user_input[7:].strip()
                    results = self.search_podcasts(keyword)
                    if results:
                        print(f"\n🔍 Found '{keyword}' in {len(results)} podcast(s):")
                        for r in sorted(results, key=lambda x: x['count'], reverse=True):
                            p = r['podcast']
                            print(f"  - {p['id']}: {r['count']} occurrences")
                    else:
                        print(f"\n❌ No results for '{keyword}'")
                    continue
                
                if user_input.lower().startswith('load '):
                    podcast_id = user_input[5:].strip()
                    podcast = self.get_podcast_by_id(podcast_id)
                    if podcast:
                        current_context_podcast = podcast
                        words = len(podcast.get('transcript', '').split())
                        print(f"\n✓ Loaded {podcast['title']} ({words:,} words) into context")
                    else:
                        print(f"\n❌ Podcast '{podcast_id}' not found")
                    continue
                
                # Process as question
                print("\n🤖 AI: ", end="", flush=True)
                response = self.process_query(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Podcast AI Agent using Ollama")
    parser.add_argument('--model', default='gemma3:latest', help='Ollama model to use')
    parser.add_argument('--api-url', default='http://localhost:5001', help='Flask API URL')
    parser.add_argument('--ollama-url', default='http://localhost:11434', help='Ollama API URL')
    
    args = parser.parse_args()
    
    # Check if Ollama is running
    try:
        response = requests.get(f"{args.ollama_url}/api/tags", timeout=2)
        response.raise_for_status()
    except:
        print("❌ Ollama is not running. Start it with: ollama serve")
        print("   Or check if it's running on a different port.")
        sys.exit(1)
    
    # Check if Flask is running
    try:
        response = requests.get(f"{args.api_url}/healthz", timeout=2)
        response.raise_for_status()
    except:
        print("❌ Flask API is not running. Start it with:")
        print("   source venv/bin/activate")
        print("   python flask_driver_runner.py app:app")
        sys.exit(1)
    
    # Initialize and run agent
    agent = PodcastAIAgent(
        flask_url=args.api_url,
        ollama_url=args.ollama_url,
        model=args.model
    )
    
    agent.run_interactive()


if __name__ == "__main__":
    main()

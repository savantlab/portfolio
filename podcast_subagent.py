#!/usr/bin/env python3
"""
Podcast Subagent - Authenticates and queries podcast transcript data.

This subagent can:
- List all available podcasts
- Retrieve specific podcast transcripts
- Search transcript content
- Analyze transcript data

Usage:
    python podcast_subagent.py list
    python podcast_subagent.py get <podcast_id>
    python podcast_subagent.py search <keyword>
    python podcast_subagent.py analyze
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PodcastSubagent:
    def __init__(self, base_url="http://localhost:5001", api_token=None, require_auth=False):
        self.base_url = base_url
        self.api_token = api_token or os.getenv('API_TOKEN')
        self.require_auth = require_auth
        
        if require_auth and not self.api_token:
            raise ValueError("API_TOKEN not found in environment")
        
        self.headers = {'Content-Type': 'application/json'}
        if self.api_token:
            self.headers['Authorization'] = f'Bearer {self.api_token}'
    
    def _request(self, endpoint, method='GET', data=None):
        """Make authenticated request to API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            sys.exit(1)
    
    def list_podcasts(self):
        """List all available podcasts"""
        podcasts = self._request('/api/podcasts')
        
        print(f"\n📻 Available Podcasts ({len(podcasts)} total)\n")
        print("=" * 80)
        
        for podcast in podcasts:
            status = "✓" if podcast.get('transcript_status') == 'success' else "✗"
            date = podcast.get('date', 'Unknown date')
            guest = podcast.get('guest', 'Unknown guest')
            word_count = len(podcast.get('transcript', '').split()) if podcast.get('transcript') else 0
            
            print(f"\n{status} {podcast['id']}")
            print(f"  Title: {podcast['title']}")
            print(f"  Guest: {guest}")
            print(f"  Date: {date}")
            print(f"  URL: {podcast['url']}")
            if word_count > 0:
                print(f"  Transcript: {word_count:,} words")
            else:
                print(f"  Transcript: Not available")
        
        print("\n" + "=" * 80)
    
    def get_podcast(self, podcast_id):
        """Get specific podcast by ID"""
        podcast = self._request(f'/api/podcasts/{podcast_id}')
        
        print(f"\n📻 {podcast['title']}\n")
        print("=" * 80)
        print(f"ID: {podcast['id']}")
        print(f"Guest: {podcast.get('guest', 'Unknown')}")
        print(f"Date: {podcast.get('date', 'Unknown')}")
        print(f"URL: {podcast['url']}")
        print(f"Description: {podcast.get('description', 'N/A')}")
        
        if podcast.get('transcript'):
            word_count = len(podcast['transcript'].split())
            print(f"\nTranscript: {word_count:,} words")
            print(f"Segments: {len(podcast.get('transcript_segments', []))} timestamped chunks")
            
            # Show first 500 characters
            print(f"\nPreview:")
            print("-" * 80)
            print(podcast['transcript'][:500] + "...")
            print("-" * 80)
        else:
            print(f"\n❌ Transcript not available: {podcast.get('transcript_error', 'Unknown error')}")
        
        return podcast
    
    def search_transcripts(self, keyword):
        """Search for keyword across all podcast transcripts"""
        podcasts = self._request('/api/podcasts')
        
        results = []
        for podcast in podcasts:
            transcript = podcast.get('transcript', '')
            if not transcript:
                continue
            
            # Case-insensitive search
            keyword_lower = keyword.lower()
            transcript_lower = transcript.lower()
            
            if keyword_lower in transcript_lower:
                # Count occurrences
                count = transcript_lower.count(keyword_lower)
                
                # Find context snippets
                snippets = []
                index = 0
                while len(snippets) < 3:  # Get up to 3 snippets
                    index = transcript_lower.find(keyword_lower, index)
                    if index == -1:
                        break
                    
                    # Extract context (50 chars before and after)
                    start = max(0, index - 50)
                    end = min(len(transcript), index + len(keyword) + 50)
                    snippet = transcript[start:end]
                    snippets.append(snippet)
                    index += 1
                
                results.append({
                    'podcast': podcast,
                    'count': count,
                    'snippets': snippets
                })
        
        if not results:
            print(f"\n❌ No results found for '{keyword}'")
            return
        
        print(f"\n🔍 Search Results for '{keyword}'\n")
        print("=" * 80)
        print(f"Found in {len(results)} podcast(s)\n")
        
        for result in sorted(results, key=lambda x: x['count'], reverse=True):
            podcast = result['podcast']
            print(f"\n📻 {podcast['title']}")
            print(f"  Guest: {podcast.get('guest', 'Unknown')}")
            print(f"  Occurrences: {result['count']}")
            print(f"  URL: {podcast['url']}")
            
            print("\n  Context snippets:")
            for i, snippet in enumerate(result['snippets'][:3], 1):
                print(f"  {i}. ...{snippet}...")
        
        print("\n" + "=" * 80)
    
    def analyze_transcripts(self):
        """Analyze all podcast transcripts for basic statistics"""
        podcasts = self._request('/api/podcasts')
        
        total_words = 0
        total_segments = 0
        podcast_stats = []
        
        for podcast in podcasts:
            if podcast.get('transcript'):
                words = len(podcast['transcript'].split())
                segments = len(podcast.get('transcript_segments', []))
                
                total_words += words
                total_segments += segments
                
                podcast_stats.append({
                    'title': podcast['title'],
                    'guest': podcast.get('guest', 'Unknown'),
                    'words': words,
                    'segments': segments
                })
        
        print(f"\n📊 Podcast Transcript Analysis\n")
        print("=" * 80)
        print(f"Total podcasts: {len(podcasts)}")
        print(f"Podcasts with transcripts: {len(podcast_stats)}")
        print(f"Total words: {total_words:,}")
        print(f"Total segments: {total_segments:,}")
        print(f"Average words per podcast: {total_words // len(podcast_stats):,}")
        
        print(f"\n📻 By Episode:\n")
        for stats in sorted(podcast_stats, key=lambda x: x['words'], reverse=True):
            print(f"  {stats['guest']}: {stats['words']:,} words ({stats['segments']} segments)")
        
        print("\n" + "=" * 80)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    try:
        agent = PodcastSubagent()
        
        if command == 'list':
            agent.list_podcasts()
        
        elif command == 'get':
            if len(sys.argv) < 3:
                print("Usage: python podcast_subagent.py get <podcast_id>")
                sys.exit(1)
            podcast_id = sys.argv[2]
            agent.get_podcast(podcast_id)
        
        elif command == 'search':
            if len(sys.argv) < 3:
                print("Usage: python podcast_subagent.py search <keyword>")
                sys.exit(1)
            keyword = ' '.join(sys.argv[2:])
            agent.search_transcripts(keyword)
        
        elif command == 'analyze':
            agent.analyze_transcripts()
        
        else:
            print(f"Unknown command: {command}")
            print(__doc__)
            sys.exit(1)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Smart Batch Transcript Fetcher

This script:
- Reads episode_list.json (all 1070+ episodes)
- Checks flask_data/podcasts.json for already-fetched transcripts
- Only fetches missing transcripts (no double calls!)
- Saves after each successful fetch (resume-friendly)
- Uses rate limiting to avoid YouTube blocks
- Shows progress and ETA

Usage:
    python fetch_transcripts_batched.py
    python fetch_transcripts_batched.py --batch-size 50
    python fetch_transcripts_batched.py --max-episodes 100
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi


class BatchTranscriptFetcher:
    def __init__(self, episode_list_file="episode_list.json", 
                 output_file="flask_data/podcasts.json",
                 batch_size=50, delay=2):
        self.episode_list_file = episode_list_file
        self.output_file = output_file
        self.batch_size = batch_size
        self.delay = delay
        self.api = YouTubeTranscriptApi()
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    def load_episode_list(self):
        """Load the full episode list"""
        if not os.path.exists(self.episode_list_file):
            print(f"❌ Episode list not found: {self.episode_list_file}")
            print("   Run: python list_peterson_episodes.py")
            sys.exit(1)
        
        with open(self.episode_list_file, 'r') as f:
            episodes = json.load(f)
        
        print(f"📋 Loaded {len(episodes)} episodes from list")
        return episodes
    
    def load_existing_transcripts(self):
        """Load already-fetched transcripts"""
        if not os.path.exists(self.output_file):
            print("📝 No existing transcripts found (starting fresh)")
            return []
        
        with open(self.output_file, 'r') as f:
            existing = json.load(f)
        
        print(f"✓ Found {len(existing)} existing transcripts")
        return existing
    
    def get_fetched_ids(self, existing_transcripts):
        """Get set of YouTube IDs that already have transcripts"""
        fetched = set()
        for entry in existing_transcripts:
            # Check if transcript was successfully fetched
            if entry.get('transcript_status') == 'success' and entry.get('transcript'):
                fetched.add(entry.get('youtube_id'))
        return fetched
    
    def fetch_transcript(self, youtube_id, retries=3):
        """Fetch transcript for a single video"""
        for attempt in range(retries):
            try:
                if attempt > 0:
                    wait_time = self.delay * (2 ** attempt)
                    time.sleep(wait_time)
                
                transcript = self.api.fetch(youtube_id, languages=['en'])
                full_text = " ".join([snippet.text for snippet in transcript.snippets])
                segments = [
                    {
                        "text": snippet.text,
                        "start": snippet.start,
                        "duration": snippet.duration
                    }
                    for snippet in transcript.snippets
                ]
                
                # Small delay to avoid rate limiting
                time.sleep(self.delay)
                
                return {
                    "full_text": full_text,
                    "segments": segments,
                    "status": "success",
                    "fetched_at": datetime.now().isoformat()
                }
            except Exception as e:
                if "Could not retrieve a transcript" in str(e):
                    if attempt < retries - 1:
                        continue
                    return {
                        "full_text": None,
                        "segments": None,
                        "status": "error",
                        "error": "Transcripts disabled or rate limited",
                        "fetched_at": datetime.now().isoformat()
                    }
                
                if attempt < retries - 1:
                    continue
                
                return {
                    "full_text": None,
                    "segments": None,
                    "status": "error",
                    "error": str(e)[:200],
                    "fetched_at": datetime.now().isoformat()
                }
    
    def create_episode_entry(self, episode_info, transcript_data):
        """Create a complete episode entry"""
        # Generate clean ID
        youtube_id = episode_info['youtube_id']
        guest = episode_info.get('guest')
        
        if guest:
            # Clean guest name for ID
            guest_clean = guest.lower().replace(' ', '-').replace(',', '').replace("'", "")
            episode_id = f"peterson-{guest_clean}"
        else:
            episode_id = f"peterson-{youtube_id}"
        
        entry = {
            "id": episode_id,
            "title": episode_info['title'],
            "date": episode_info.get('date'),
            "guest": guest,
            "youtube_id": youtube_id,
            "url": episode_info['url'],
            "views": episode_info.get('views'),
            "duration": episode_info.get('duration'),
            "description": episode_info['title'],
            "transcript": transcript_data["full_text"],
            "transcript_segments": transcript_data["segments"],
            "transcript_status": transcript_data["status"],
            "fetched_at": transcript_data.get("fetched_at")
        }
        
        if "error" in transcript_data:
            entry["transcript_error"] = transcript_data["error"]
        
        return entry
    
    def save_transcripts(self, transcripts):
        """Save transcripts to JSON file"""
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(transcripts, f, indent=2, ensure_ascii=False)
    
    def run(self, max_episodes=None):
        """Run the batch fetcher"""
        print("\n" + "="*80)
        print("Smart Batch Transcript Fetcher")
        print("="*80)
        print(f"Batch size: {self.batch_size}")
        print(f"Delay: {self.delay}s between requests")
        print(f"Output: {self.output_file}")
        print("="*80 + "\n")
        
        # Load data
        all_episodes = self.load_episode_list()
        existing_transcripts = self.load_existing_transcripts()
        fetched_ids = self.get_fetched_ids(existing_transcripts)
        
        # Find episodes that need transcripts
        to_fetch = [ep for ep in all_episodes if ep['youtube_id'] not in fetched_ids]
        
        if max_episodes:
            to_fetch = to_fetch[:max_episodes]
        
        print(f"\n📊 Status:")
        print(f"   Total episodes: {len(all_episodes)}")
        print(f"   Already fetched: {len(fetched_ids)}")
        print(f"   Need to fetch: {len(to_fetch)}")
        
        if not to_fetch:
            print("\n✓ All episodes already have transcripts!")
            return
        
        # Estimate time
        estimated_seconds = len(to_fetch) * (self.delay + 2)
        estimated_minutes = estimated_seconds / 60
        print(f"   Estimated time: ~{estimated_minutes:.1f} minutes")
        print()
        
        # Create lookup for existing transcripts by youtube_id
        existing_by_id = {t['youtube_id']: t for t in existing_transcripts if 'youtube_id' in t}
        
        # Fetch transcripts
        fetched_count = 0
        error_count = 0
        start_time = time.time()
        
        for i, episode_info in enumerate(to_fetch, 1):
            youtube_id = episode_info['youtube_id']
            title = episode_info['title']
            
            # Progress indicator
            progress = (i / len(to_fetch)) * 100
            elapsed = time.time() - start_time
            rate = i / elapsed if elapsed > 0 else 0
            eta_seconds = (len(to_fetch) - i) / rate if rate > 0 else 0
            eta_minutes = eta_seconds / 60
            
            print(f"[{i}/{len(to_fetch)} - {progress:.1f}%] Fetching: {title[:60]}")
            print(f"   ETA: {eta_minutes:.1f}m | Rate: {rate:.2f} eps/sec | ID: {youtube_id}")
            
            # Fetch transcript
            transcript_data = self.fetch_transcript(youtube_id)
            
            # Create entry
            episode_entry = self.create_episode_entry(episode_info, transcript_data)
            
            # Update or add to transcripts
            if youtube_id in existing_by_id:
                # Update existing entry
                idx = existing_transcripts.index(existing_by_id[youtube_id])
                existing_transcripts[idx] = episode_entry
            else:
                # Add new entry
                existing_transcripts.append(episode_entry)
            
            # Track stats
            if transcript_data["status"] == "success":
                word_count = len(transcript_data["full_text"].split())
                print(f"   ✓ Success: {word_count:,} words\n")
                fetched_count += 1
            else:
                print(f"   ❌ Error: {transcript_data.get('error', 'Unknown')}\n")
                error_count += 1
            
            # Save after each fetch (resume-friendly!)
            self.save_transcripts(existing_transcripts)
            
            # Batch pause (every N episodes)
            if i % self.batch_size == 0 and i < len(to_fetch):
                print(f"\n{'='*80}")
                print(f"Batch checkpoint: {i}/{len(to_fetch)} complete")
                print(f"Success: {fetched_count} | Errors: {error_count}")
                print(f"Pausing 10 seconds to avoid rate limiting...")
                print(f"{'='*80}\n")
                time.sleep(10)
        
        # Final summary
        total_time = time.time() - start_time
        print("\n" + "="*80)
        print("Summary")
        print("="*80)
        print(f"Episodes processed: {len(to_fetch)}")
        print(f"Successful: {fetched_count}")
        print(f"Errors: {error_count}")
        print(f"Total time: {total_time/60:.1f} minutes")
        print(f"Average: {total_time/len(to_fetch):.1f} seconds per episode")
        print(f"\nTotal in database: {len(existing_transcripts)} episodes")
        success_total = sum(1 for t in existing_transcripts if t.get('transcript_status') == 'success')
        print(f"With transcripts: {success_total}")
        print(f"Saved to: {self.output_file}")
        print("="*80)


def main():
    parser = argparse.ArgumentParser(description="Smart batch transcript fetcher")
    parser.add_argument('--batch-size', type=int, default=50, help='Pause after N episodes')
    parser.add_argument('--delay', type=int, default=2, help='Seconds between requests')
    parser.add_argument('--max-episodes', type=int, help='Max episodes to fetch (for testing)')
    parser.add_argument('--episode-list', default='episode_list.json', help='Input episode list')
    parser.add_argument('--output', default='flask_data/podcasts.json', help='Output file')
    
    args = parser.parse_args()
    
    fetcher = BatchTranscriptFetcher(
        episode_list_file=args.episode_list,
        output_file=args.output,
        batch_size=args.batch_size,
        delay=args.delay
    )
    
    fetcher.run(max_episodes=args.max_episodes)


if __name__ == "__main__":
    main()

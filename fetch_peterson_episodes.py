#!/usr/bin/env python3
"""
Fetch all Jordan Peterson podcast episodes.

This script:
- Fetches Peterson's podcast feed (YouTube channel or RSS)
- Extracts episode metadata and YouTube IDs
- Downloads transcripts for each episode
- Saves to JSON for the Flask API

Usage:
    python fetch_peterson_episodes.py
    python fetch_peterson_episodes.py --limit 10  # Fetch only 10 most recent
    python fetch_peterson_episodes.py --channel @JordanBPeterson
"""

import os
import sys
import json
import argparse
import requests
import scrapetube
import time
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime


class PetersonPodcastFetcher:
    def __init__(self, output_file="flask_data/podcasts.json"):
        self.output_file = output_file
        self.api = YouTubeTranscriptApi()
    
    def fetch_from_youtube_channel(self, channel_id, max_results=None):
        """
        Fetch ALL episodes from YouTube channel using scrapetube.
        No API key required!
        """
        print(f"📡 Fetching episodes from YouTube channel: {channel_id}")
        print("   Using scrapetube (no API key needed)...")
        
        episodes = []
        
        try:
            # Fetch videos from channel
            videos = scrapetube.get_channel(channel_username=channel_id.replace('@', ''))
            
            count = 0
            for video in videos:
                if max_results and count >= max_results:
                    break
                
                video_id = video['videoId']
                title = video['title']['runs'][0]['text']
                
                # Try to extract date (published date)
                date = None
                try:
                    if 'publishedTimeText' in video:
                        date_text = video['publishedTimeText']['simpleText']
                        # This is relative like "2 months ago", not absolute
                        # For now, leave as None
                except:
                    pass
                
                # Try to extract guest from title
                guest = None
                if '|' in title:
                    parts = title.split('|')
                    if len(parts) > 1:
                        guest = parts[1].strip()
                elif ' with ' in title.lower():
                    # Extract guest after "with"
                    parts = title.lower().split(' with ')
                    if len(parts) > 1:
                        guest = parts[1].strip().title()
                
                episodes.append((video_id, title, guest, date))
                count += 1
            
            print(f"   ✓ Found {len(episodes)} episodes")
            
        except Exception as e:
            print(f"   ❌ Error fetching from YouTube: {e}")
            print("   Falling back to manual list...")
            
            # Fallback to manual list
            episodes = [
                ("urk9BJIxZ3U", "Jordan Peterson & Peter Thiel", "Peter Thiel", "2025-09-30"),
                ("Rop6FnLD01o", "Jordan Peterson & Gad Saad", "Gad Saad", None),
                ("aa0cLA0Gm0M", "Jordan Peterson & Dan Crenshaw", "Dan Crenshaw", None),
                ("iRREGG6hLVU", "Jordan Peterson & Ben Shapiro", "Ben Shapiro", None),
            ]
        
        return episodes
    
    def fetch_transcript(self, youtube_id, retries=3, delay=2):
        """Fetch transcript for a YouTube video with retries and rate limiting"""
        for attempt in range(retries):
            try:
                # Rate limiting between attempts
                if attempt > 0:
                    wait_time = delay * (2 ** attempt)  # Exponential backoff
                    print(f"  Waiting {wait_time}s before retry...")
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
                
                # Small delay even on success to avoid rate limiting
                time.sleep(1)
                
                return {
                    "full_text": full_text,
                    "segments": segments,
                    "status": "success"
                }
            except Exception as e:
                error_msg = str(e)
                
                # Check if it's an IP block
                if "Could not retrieve a transcript" in error_msg:
                    if attempt < retries - 1:
                        print(f"  Rate limited, retry {attempt + 1}/{retries}...")
                        continue
                    # Store simplified error
                    return {
                        "full_text": None,
                        "segments": None,
                        "status": "error",
                        "error": "Transcripts disabled or rate limited"
                    }
                
                if attempt < retries - 1:
                    print(f"  Retry {attempt + 1}/{retries}...")
                    continue
                
                return {
                    "full_text": None,
                    "segments": None,
                    "status": "error",
                    "error": error_msg[:200]  # Truncate long errors
                }
    
    def create_episode_entry(self, youtube_id, title, guest, date):
        """Create a podcast episode entry with transcript"""
        episode_id = f"peterson-{guest.lower().replace(' ', '-')}" if guest else f"peterson-{youtube_id}"
        
        print(f"\n📻 Fetching: {title}")
        print(f"   YouTube ID: {youtube_id}")
        
        transcript_data = self.fetch_transcript(youtube_id)
        
        entry = {
            "id": episode_id,
            "title": title,
            "date": date,
            "guest": guest,
            "youtube_id": youtube_id,
            "url": f"https://www.youtube.com/watch?v={youtube_id}",
            "description": f"Peterson podcast episode with {guest}" if guest else "Peterson podcast episode",
            "transcript": transcript_data["full_text"],
            "transcript_segments": transcript_data["segments"],
            "transcript_status": transcript_data["status"]
        }
        
        if "error" in transcript_data:
            entry["transcript_error"] = transcript_data["error"]
            print(f"   ❌ Error: {transcript_data['error']}")
        else:
            word_count = len(transcript_data["full_text"].split()) if transcript_data["full_text"] else 0
            print(f"   ✓ Success: {word_count:,} words")
        
        return entry
    
    def fetch_all(self, limit=None):
        """Fetch all episodes and their transcripts"""
        print("="*80)
        print("Jordan Peterson Podcast Fetcher")
        print("="*80)
        
        # Get episode list
        episodes = self.fetch_from_youtube_channel("@JordanBPeterson", max_results=limit or 100)
        
        if limit:
            episodes = episodes[:limit]
        
        print(f"\n📋 Found {len(episodes)} episodes to process")
        
        # Fetch transcripts for each
        results = []
        for youtube_id, title, guest, date in episodes:
            entry = self.create_episode_entry(youtube_id, title, guest, date)
            results.append(entry)
        
        # Save to JSON
        print(f"\n💾 Saving to {self.output_file}...")
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved {len(results)} episodes")
        
        # Statistics
        success_count = sum(1 for r in results if r.get('transcript_status') == 'success')
        total_words = sum(len(r.get('transcript', '').split()) for r in results if r.get('transcript'))
        
        print("\n" + "="*80)
        print("Summary")
        print("="*80)
        print(f"Total episodes: {len(results)}")
        print(f"Successful transcripts: {success_count}")
        print(f"Failed transcripts: {len(results) - success_count}")
        print(f"Total words: {total_words:,}")
        print(f"Average words per episode: {total_words // success_count if success_count else 0:,}")
        print("="*80)
        
        return results


def main():
    parser = argparse.ArgumentParser(description="Fetch Jordan Peterson podcast episodes")
    parser.add_argument('--limit', type=int, help='Limit number of episodes to fetch')
    parser.add_argument('--output', default='flask_data/podcasts.json', help='Output JSON file')
    parser.add_argument('--channel', default='@JordanBPeterson', help='YouTube channel ID')
    
    args = parser.parse_args()
    
    fetcher = PetersonPodcastFetcher(output_file=args.output)
    fetcher.fetch_all(limit=args.limit)


if __name__ == "__main__":
    main()

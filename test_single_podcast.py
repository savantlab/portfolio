#!/usr/bin/env python3
"""
Test script: Fetch ONE random podcast transcript and show the response.

Usage:
    python test_single_podcast.py
    python test_single_podcast.py --video-id urk9BJIxZ3U
"""

import json
import random
import argparse
from youtube_transcript_api import YouTubeTranscriptApi


def fetch_random_podcast():
    """Fetch a random podcast from the episode list"""
    # Load episode list
    try:
        with open('episode_list.json', 'r') as f:
            episodes = json.load(f)
    except FileNotFoundError:
        print("❌ episode_list.json not found")
        print("   Run: python list_peterson_episodes.py")
        return None
    
    # Pick random episode
    episode = random.choice(episodes)
    return episode


def fetch_single_transcript(youtube_id):
    """Fetch transcript for a single video"""
    print(f"📡 Fetching transcript for: {youtube_id}")
    print(f"   URL: https://www.youtube.com/watch?v={youtube_id}\n")
    
    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(youtube_id, languages=['en'])
        
        # Convert to dict format
        full_text = " ".join([snippet.text for snippet in transcript.snippets])
        segments = [
            {
                "text": snippet.text,
                "start": snippet.start,
                "duration": snippet.duration
            }
            for snippet in transcript.snippets
        ]
        
        return {
            "status": "success",
            "full_text": full_text,
            "segments": segments,
            "segment_count": len(segments),
            "word_count": len(full_text.split()),
            "char_count": len(full_text)
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(description="Test single podcast transcript fetch")
    parser.add_argument('--video-id', help='Specific YouTube video ID to test')
    args = parser.parse_args()
    
    print("="*80)
    print("Single Podcast Transcript Test")
    print("="*80 + "\n")
    
    if args.video_id:
        youtube_id = args.video_id
        title = "Manual selection"
    else:
        # Get random episode
        episode = fetch_random_podcast()
        if not episode:
            return
        
        youtube_id = episode['youtube_id']
        title = episode['title']
        
        print(f"🎲 Random episode selected:")
        print(f"   Title: {title}")
        print(f"   ID: {youtube_id}")
        print(f"   URL: {episode['url']}\n")
    
    # Fetch transcript
    result = fetch_single_transcript(youtube_id)
    
    # Display results
    print("="*80)
    print("Response")
    print("="*80 + "\n")
    
    if result["status"] == "success":
        print(f"✓ Status: {result['status']}")
        print(f"✓ Segments: {result['segment_count']}")
        print(f"✓ Word count: {result['word_count']:,}")
        print(f"✓ Character count: {result['char_count']:,}\n")
        
        # Show first 500 characters
        print("First 500 characters:")
        print("-"*80)
        print(result['full_text'][:500])
        print("...")
        print("-"*80 + "\n")
        
        # Show first 3 segments with timestamps
        print("First 3 segments:")
        print("-"*80)
        for i, seg in enumerate(result['segments'][:3], 1):
            timestamp = f"{seg['start']:.1f}s"
            print(f"{i}. [{timestamp}] {seg['text']}")
        print("-"*80 + "\n")
        
        # Save to file
        output_file = f"test_transcript_{youtube_id}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Full response saved to: {output_file}")
        
    else:
        print(f"❌ Status: {result['status']}")
        print(f"❌ Error: {result['error']}\n")
        
        print("This might be because:")
        print("  - Transcripts are disabled for this video")
        print("  - Your IP is rate-limited by YouTube")
        print("  - The video doesn't have captions")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    main()

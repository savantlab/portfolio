#!/usr/bin/env python3
"""
List all Jordan Peterson podcast episodes (WITHOUT fetching transcripts).

This is much faster - just gets the episode list.
Use this first to see how many episodes exist, then fetch transcripts separately.

Usage:
    python list_peterson_episodes.py
    python list_peterson_episodes.py --output episode_list.json
    python list_peterson_episodes.py --limit 50
"""

import os
import sys
import json
import argparse
import scrapetube


def list_episodes(channel_id="@JordanBPeterson", max_results=None):
    """List all episodes from YouTube channel"""
    print(f"📡 Fetching episode list from: {channel_id}")
    print("   (Not fetching transcripts - just metadata)\n")
    
    episodes = []
    
    try:
        videos = scrapetube.get_channel(channel_username=channel_id.replace('@', ''))
        
        count = 0
        for video in videos:
            if max_results and count >= max_results:
                break
            
            video_id = video['videoId']
            title = video['title']['runs'][0]['text']
            
            # Get view count if available
            views = None
            try:
                if 'viewCountText' in video:
                    views = video['viewCountText']['simpleText']
            except:
                pass
            
            # Get duration if available
            duration = None
            try:
                if 'lengthText' in video:
                    duration = video['lengthText']['simpleText']
            except:
                pass
            
            # Try to extract guest from title
            guest = None
            if '|' in title:
                parts = title.split('|')
                if len(parts) > 1:
                    guest = parts[1].strip()
            elif ' with ' in title.lower():
                parts = title.lower().split(' with ')
                if len(parts) > 1:
                    guest = parts[1].strip().title()
            
            episode = {
                "youtube_id": video_id,
                "title": title,
                "guest": guest,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "views": views,
                "duration": duration
            }
            
            episodes.append(episode)
            count += 1
            
            # Print progress every 10 episodes
            if count % 10 == 0:
                print(f"   Found {count} episodes...")
        
        print(f"\n✓ Found {len(episodes)} total episodes\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []
    
    return episodes


def main():
    parser = argparse.ArgumentParser(description="List Jordan Peterson podcast episodes (fast - no transcripts)")
    parser.add_argument('--limit', type=int, help='Limit number of episodes')
    parser.add_argument('--output', default='episode_list.json', help='Output JSON file')
    parser.add_argument('--channel', default='@JordanBPeterson', help='YouTube channel')
    
    args = parser.parse_args()
    
    episodes = list_episodes(args.channel, args.limit)
    
    if episodes:
        # Save to JSON
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(episodes, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved to: {args.output}\n")
        
        # Print summary
        print("="*80)
        print("Summary")
        print("="*80)
        print(f"Total episodes: {len(episodes)}")
        print(f"Output file: {args.output}")
        print("\nSample episodes:")
        for ep in episodes[:5]:
            guest = f" (Guest: {ep['guest']})" if ep['guest'] else ""
            print(f"  - {ep['title']}{guest}")
            print(f"    {ep['url']}")
        if len(episodes) > 5:
            print(f"  ... and {len(episodes) - 5} more")
        print("="*80)
        
        print("\nNext steps:")
        print(f"1. Review the list in {args.output}")
        print("2. Fetch transcripts: python fetch_peterson_episodes.py")
        print("   (This will take longer - fetches one transcript at a time)")
    else:
        print("No episodes found")
        sys.exit(1)


if __name__ == "__main__":
    main()

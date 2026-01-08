#!/usr/bin/env python3
"""
YouTube Transcript Rate Limit Checker

Tests multiple videos to see:
- Which ones have transcripts available
- If we're being rate limited
- Success rate
- Response times

Usage:
    python check_rate_limit.py
    python check_rate_limit.py --test-count 10
"""

import json
import time
import argparse
from datetime import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound


def load_test_videos(count=5):
    """Load a sample of videos to test"""
    try:
        with open('episode_list.json', 'r') as f:
            episodes = json.load(f)
        return episodes[:count]
    except FileNotFoundError:
        # Fallback to known IDs
        return [
            {"youtube_id": "urk9BJIxZ3U", "title": "Peterson & Thiel"},
            {"youtube_id": "Rop6FnLD01o", "title": "Peterson & Saad"},
            {"youtube_id": "aa0cLA0Gm0M", "title": "Peterson & Crenshaw"},
            {"youtube_id": "iRREGG6hLVU", "title": "Peterson & Shapiro"},
            {"youtube_id": "nlgG8C1GydA", "title": "Peterson & Blackwood"}
        ][:count]


def test_single_video(youtube_id, attempt_num):
    """Test fetching transcript for a single video"""
    start_time = time.time()
    
    result = {
        "video_id": youtube_id,
        "attempt": attempt_num,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(youtube_id, languages=['en'])
        
        elapsed = time.time() - start_time
        word_count = len(" ".join([s.text for s in transcript.snippets]).split())
        
        result.update({
            "status": "success",
            "response_time": round(elapsed, 2),
            "segment_count": len(transcript.snippets),
            "word_count": word_count
        })
        
    except TranscriptsDisabled:
        result.update({
            "status": "disabled",
            "error_type": "TranscriptsDisabled",
            "error": "Transcripts are disabled for this video"
        })
    
    except NoTranscriptFound:
        result.update({
            "status": "not_found",
            "error_type": "NoTranscriptFound",
            "error": "No transcript found (no captions available)"
        })
    
    except Exception as e:
        error_str = str(e)
        
        # Categorize error
        if "Could not retrieve a transcript" in error_str:
            if "blocking requests from your IP" in error_str:
                error_type = "IP_BLOCKED"
                status = "ip_blocked"
            else:
                error_type = "RETRIEVAL_FAILED"
                status = "failed"
        else:
            error_type = "UNKNOWN"
            status = "error"
        
        result.update({
            "status": status,
            "error_type": error_type,
            "error": error_str[:200]  # Truncate long errors
        })
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Check YouTube transcript rate limit status")
    parser.add_argument('--test-count', type=int, default=5, help='Number of videos to test')
    parser.add_argument('--delay', type=float, default=2.0, help='Seconds between tests')
    args = parser.parse_args()
    
    print("="*80)
    print("YouTube Transcript Rate Limit Checker")
    print("="*80)
    print(f"Testing {args.test_count} videos with {args.delay}s delay between requests\n")
    
    # Load test videos
    test_videos = load_test_videos(args.test_count)
    
    results = []
    success_count = 0
    rate_limited_count = 0
    other_error_count = 0
    
    for i, video in enumerate(test_videos, 1):
        video_id = video['youtube_id']
        title = video.get('title', 'Unknown')
        
        print(f"[{i}/{len(test_videos)}] Testing: {title[:50]}")
        print(f"           ID: {video_id}")
        
        result = test_single_video(video_id, i)
        results.append(result)
        
        # Display result
        if result['status'] == 'success':
            print(f"           ✓ Success: {result['word_count']:,} words in {result['response_time']}s")
            success_count += 1
        elif result['status'] == 'ip_blocked':
            print(f"           ❌ IP Blocked by YouTube")
            rate_limited_count += 1
        elif result['status'] == 'rate_limited':
            print(f"           ⚠️  Rate limited")
            rate_limited_count += 1
        elif result['status'] == 'disabled':
            print(f"           ⊘ Transcripts disabled")
            other_error_count += 1
        elif result['status'] == 'not_found':
            print(f"           ⊘ No captions available")
            other_error_count += 1
        else:
            print(f"           ❌ Error: {result['error_type']}")
            other_error_count += 1
        
        print()
        
        # Delay between requests
        if i < len(test_videos):
            time.sleep(args.delay)
    
    # Summary
    print("="*80)
    print("Summary")
    print("="*80)
    print(f"Total tests: {len(results)}")
    print(f"✓ Successful: {success_count} ({success_count/len(results)*100:.1f}%)")
    print(f"❌ Rate limited: {rate_limited_count} ({rate_limited_count/len(results)*100:.1f}%)")
    print(f"⊘ Other errors: {other_error_count} ({other_error_count/len(results)*100:.1f}%)")
    
    # Diagnosis
    print("\n" + "="*80)
    print("Diagnosis")
    print("="*80)
    
    if success_count == len(results):
        print("✓ All tests passed - no rate limiting detected!")
        print("  You can proceed with batch fetching.")
    
    elif success_count > 0:
        print(f"⚠️  Partial success ({success_count}/{len(results)} working)")
        print("  Some videos work, others don't.")
        print("  Possible causes:")
        print("  - Some videos don't have transcripts enabled")
        print("  - Approaching rate limit threshold")
        print("\n  Recommendation:")
        print("  - Use longer delays (--delay 5)")
        print("  - Fetch in smaller batches")
    
    elif rate_limited_count > 0:
        print("❌ Rate limited - YouTube is blocking your IP")
        print("\n  Why this happens:")
        print("  - Too many requests in short time")
        print("  - IP is flagged by YouTube")
        print("  - Shared IP (VPN, cloud provider, etc.)")
        print("\n  Solutions:")
        print("  1. Wait 30-60 minutes before trying again")
        print("  2. Use a different network (mobile hotspot, different WiFi)")
        print("  3. Use VPN to get different IP")
        print("  4. Increase delay between requests (--delay 10)")
        print("  5. Run overnight when usage is lower")
    
    else:
        print("⚠️  All tests failed with other errors")
        print("  Check the error details above")
    
    # Save detailed results
    output_file = f"rate_limit_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: {output_file}")
    print("="*80)
    
    # Recommendations based on results
    if success_count == 0 and rate_limited_count > 0:
        print("\n⏰ WAIT RECOMMENDATION:")
        print("   Wait at least 30 minutes before trying again")
        print("   Or switch to a different network/VPN")


if __name__ == "__main__":
    main()

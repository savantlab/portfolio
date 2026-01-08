#!/usr/bin/env python3
"""
Fetch YouTube transcripts for podcast episodes and save to JSON.
"""

import json
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

# Podcast episodes from resume
PODCASTS = [
    {
        "id": "peterson-thiel-2025",
        "title": "Jordan Peterson & Peter Thiel",
        "date": "2025-09-30",
        "guest": "Peter Thiel",
        "youtube_id": "urk9BJIxZ3U",
        "url": "https://www.youtube.com/watch?v=urk9BJIxZ3U",
        "description": "Last appearance on Peterson's podcast"
    },
    {
        "id": "peterson-saad",
        "title": "Jordan Peterson & Gad Saad",
        "date": None,
        "guest": "Gad Saad",
        "youtube_id": "Rop6FnLD01o",
        "url": "https://www.youtube.com/watch?v=Rop6FnLD01o",
        "description": "Peterson podcast episode with Gad Saad"
    },
    {
        "id": "peterson-crenshaw",
        "title": "Jordan Peterson & Dan Crenshaw",
        "date": None,
        "guest": "Dan Crenshaw",
        "youtube_id": "aa0cLA0Gm0M",
        "url": "https://www.youtube.com/watch?v=aa0cLA0Gm0M",
        "description": "Peterson podcast episode with Dan Crenshaw (House Intelligence Committee)"
    },
    {
        "id": "peterson-shapiro",
        "title": "Jordan Peterson & Ben Shapiro",
        "date": None,
        "guest": "Ben Shapiro",
        "youtube_id": "iRREGG6hLVU",
        "url": "https://www.youtube.com/watch?v=iRREGG6hLVU",
        "description": "Peterson podcast episode with Ben Shapiro"
    }
]


def fetch_transcript(youtube_id):
    """Fetch transcript for a YouTube video."""
    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(youtube_id, languages=['en'])
        # Combine all text segments
        full_text = " ".join([snippet.text for snippet in transcript.snippets])
        # Convert snippets to dicts for JSON serialization
        segments = [
            {
                "text": snippet.text,
                "start": snippet.start,
                "duration": snippet.duration
            }
            for snippet in transcript.snippets
        ]
        return {
            "full_text": full_text,
            "segments": segments,
            "status": "success"
        }
    except TranscriptsDisabled:
        return {
            "full_text": None,
            "segments": None,
            "status": "error",
            "error": "Transcripts are disabled for this video"
        }
    except NoTranscriptFound:
        return {
            "full_text": None,
            "segments": None,
            "status": "error",
            "error": "No transcript found for this video"
        }
    except Exception as e:
        return {
            "full_text": None,
            "segments": None,
            "status": "error",
            "error": str(e)
        }


def main():
    """Fetch all transcripts and save to JSON."""
    results = []
    
    for podcast in PODCASTS:
        print(f"Fetching transcript for: {podcast['title']} ({podcast['youtube_id']})")
        
        transcript_data = fetch_transcript(podcast['youtube_id'])
        
        # Combine metadata with transcript
        podcast_entry = {
            **podcast,
            "transcript": transcript_data["full_text"],
            "transcript_segments": transcript_data["segments"],
            "transcript_status": transcript_data["status"]
        }
        
        if "error" in transcript_data:
            podcast_entry["transcript_error"] = transcript_data["error"]
            print(f"  ❌ Error: {transcript_data['error']}")
        else:
            word_count = len(transcript_data["full_text"].split())
            print(f"  ✓ Success: {word_count:,} words")
        
        results.append(podcast_entry)
    
    # Save to flask_data/podcasts.json
    output_path = "flask_data/podcasts.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Saved {len(results)} podcast entries to {output_path}")


if __name__ == "__main__":
    main()

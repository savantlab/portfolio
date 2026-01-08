# Fetching All Peterson Podcast Episodes

Peterson has **1,070+ episodes** on his YouTube channel. Here's how to get them all.

## Overview

**Challenge:** YouTube rate-limits transcript requests from single IPs
**Solution:** Two-phase approach + rate limiting

## Phase 1: Get Episode List (Fast ⚡)

First, get the list of ALL episodes WITHOUT transcripts:

```bash
source venv/bin/activate
python list_peterson_episodes.py
```

This creates `episode_list.json` with metadata for all 1,070+ episodes:
- YouTube IDs
- Titles
- Guest names (extracted)
- URLs
- View counts
- Durations

**Speed:** ~30 seconds for 1,070 episodes

## Phase 2: Fetch Transcripts (Slow 🐌)

Now fetch transcripts in batches to avoid rate limiting:

### Option A: Fetch in Small Batches (Recommended)

```bash
# Fetch first 50 episodes
python fetch_peterson_episodes.py --limit 50

# Wait 10-15 minutes to avoid rate limiting
sleep 900

# Fetch next 50 (episodes 51-100)
# You'll need to modify the script to skip first 50
```

### Option B: Fetch All at Once (Risk of Rate Limit)

```bash
# This will take HOURS and may hit rate limits
python fetch_peterson_episodes.py
```

**Time estimate:** 
- 1,070 episodes × 3 seconds per episode = ~53 minutes minimum
- With rate limiting/retries: **2-4 hours**

### Option C: Use Batch Script (Best)

I'll create a batch script that fetches in chunks with delays:

```bash
./fetch_all_episodes_batched.sh
```

## Rate Limiting Issues

YouTube blocks IPs that make too many transcript requests:

**Symptoms:**
- "Could not retrieve a transcript" errors
- "Your IP has been blocked" messages

**Solutions:**

1. **Wait longer between requests** (script does 1-2 second delays)
2. **Use VPN/proxy** to change IP
3. **Fetch in smaller batches** (50-100 at a time)
4. **Use multiple machines** to distribute load
5. **Run overnight** when usage is lower

## What You Get

### Episode List (`episode_list.json`)
```json
[
  {
    "youtube_id": "IsXdO5RD_NU",
    "title": "Understanding the True Spirit of Christmas",
    "guest": null,
    "url": "https://www.youtube.com/watch?v=IsXdO5RD_NU",
    "views": "50K views",
    "duration": "15:32"
  },
  ...1070 episodes
]
```

### Full Transcripts (`flask_data/podcasts.json`)
```json
[
  {
    "id": "peterson-IsXdO5RD_NU",
    "title": "Understanding the True Spirit of Christmas",
    "youtube_id": "IsXdO5RD_NU",
    "transcript": "full text of 15-minute video...",
    "transcript_segments": [...],
    "transcript_status": "success"
  },
  ...
]
```

## Realistic Workflow

### Day 1: Setup
```bash
# Get episode list (30 seconds)
python list_peterson_episodes.py

# Review the list
cat episode_list.json | jq length  # Shows 1070
cat episode_list.json | jq '.[0:5]'  # First 5 episodes
```

### Day 2-4: Fetch Transcripts in Batches

**Morning (50 episodes):**
```bash
python fetch_peterson_episodes.py --limit 50
```

**Afternoon (next 50):**
You'll need to either:
1. Edit `fetch_peterson_episodes.py` to skip first 50
2. Or use the batch script I'll create

**Evening (next 50):**
Continue...

**Repeat** until all 1,070 episodes are fetched.

## Batch Fetching Script

Let me create a script that handles this automatically:

```bash
./fetch_all_episodes_batched.sh
```

This will:
1. Read `episode_list.json`
2. Fetch transcripts in batches of 50
3. Wait 15 minutes between batches
4. Resume if interrupted
5. Save progress after each batch

## Storage Requirements

- **Episode list only:** ~500 KB
- **All 1,070 transcripts:** ~50-100 MB (estimated)
- **Average transcript:** ~50 KB per episode

## Processing All Episodes

Once you have all transcripts:

```bash
# Run analysis on ALL episodes
./run_fresh_analysis.sh

# This will take MANY hours with 1,070 episodes
# Estimated: 1,070 × 4 analyses × 30 seconds = ~35 hours
```

**Recommendation:** Start with smaller batches for analysis too!

## Selective Fetching

You probably don't need ALL 1,070 episodes. Consider:

### Podcasts Only (Not Lectures)
Filter `episode_list.json` for podcast episodes:
```bash
cat episode_list.json | jq '[.[] | select(.title | contains("EP ") or contains("podcast"))]' > podcasts_only.json
```

### Recent Episodes Only
```bash
# First 100 (most recent)
python fetch_peterson_episodes.py --limit 100
```

### Specific Guests
```bash
# Filter for specific guests
cat episode_list.json | jq '[.[] | select(.guest != null)]' > episodes_with_guests.json
```

## Next Steps

1. **List episodes:** `python list_peterson_episodes.py`
2. **Review list:** `cat episode_list.json | jq`
3. **Decide strategy:**
   - All 1,070? (multi-day process)
   - Podcasts only? (~200-300 episodes)
   - Recent only? (50-100 episodes)
4. **Fetch transcripts** in batches
5. **Run analysis** on collected data

## Tips for Success

✅ **Start small** - Test with 10-20 episodes first
✅ **Monitor progress** - Check `flask_data/podcasts.json` size
✅ **Use batches** - 50-100 episodes at a time with breaks
✅ **Run overnight** - Less competition for YouTube's resources
✅ **Be patient** - 1,070 episodes takes time
✅ **Focus on podcasts** - Lectures may be less relevant

## Troubleshooting

**"All transcripts failing"**
- You've hit rate limit
- Wait 30-60 minutes
- Try from different network/VPN

**"Script hangs"**
- YouTube may be slow
- Ctrl+C and restart with smaller batch

**"Running out of disk space"**
- Each transcript ~50 KB
- 1,070 × 50 KB = ~53 MB total
- Should be fine unless your disk is nearly full

## Files Reference

| File | Purpose | Size |
|------|---------|------|
| `list_peterson_episodes.py` | Fast episode lister | - |
| `fetch_peterson_episodes.py` | Transcript fetcher | - |
| `episode_list.json` | All episode metadata | ~500 KB |
| `flask_data/podcasts.json` | Episodes + transcripts | ~50-100 MB |

## Summary

**1,070 episodes** is a LOT of data!

**Quick start:**
```bash
# 1. Get the list (30 seconds)
python list_peterson_episodes.py

# 2. Review what you have
cat episode_list.json | jq length

# 3. Start with a small batch
python fetch_peterson_episodes.py --limit 20

# 4. Scale up gradually
```

**Recommended approach:**
- Focus on podcast episodes only (~200-300)
- Fetch in batches of 50
- Take breaks between batches
- Analyze as you go

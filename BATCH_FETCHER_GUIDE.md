# Smart Batch Fetcher Guide

The smart way to fetch all 1,070 Peterson episodes without double-calling.

## How It Works

```
┌──────────────────┐
│ episode_list.json│  (All 1070 episodes)
└────────┬─────────┘
         │
         ▼
┌──────────────────────────┐
│ Check existing:          │
│ flask_data/podcasts.json │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Only fetch MISSING ones  │
│ (No double calls!)       │
└────────┬─────────────────┘
         │
         ▼
┌──────────────────────────┐
│ Save after EACH episode  │
│ (Resume-friendly!)       │
└──────────────────────────┘
```

## Key Features

✅ **No double calls** - Checks what's already fetched
✅ **Resume-friendly** - Saves after each episode
✅ **Progress tracking** - Shows ETA and rate
✅ **Batch pauses** - 10s pause every 50 episodes
✅ **Rate limiting** - 2s delay between requests
✅ **Error handling** - Retries with exponential backoff

## Usage

### Test with 5 Episodes
```bash
source venv/bin/activate
python fetch_transcripts_batched.py --max-episodes 5
```

### Fetch 100 Episodes
```bash
python fetch_transcripts_batched.py --max-episodes 100
```

### Fetch ALL 1,070 Episodes
```bash
python fetch_transcripts_batched.py
```

### Resume After Interruption
Just run it again - it automatically skips already-fetched episodes:
```bash
python fetch_transcripts_batched.py
```

## Command Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--max-episodes N` | None | Fetch only N episodes (for testing) |
| `--batch-size N` | 50 | Pause every N episodes |
| `--delay N` | 2 | Seconds between requests |
| `--episode-list FILE` | `episode_list.json` | Input file |
| `--output FILE` | `flask_data/podcasts.json` | Output file |

## Example Workflow

### Day 1: Get the list
```bash
python list_peterson_episodes.py
# Creates episode_list.json with 1070 episodes
```

### Day 2: Start fetching
```bash
# Morning: Fetch first 100
python fetch_transcripts_batched.py --max-episodes 100

# Status check
cat flask_data/podcasts.json | jq 'length'
```

### Day 3: Continue
```bash
# It automatically skips the first 100!
python fetch_transcripts_batched.py --max-episodes 200

# Now you have 200 episodes
```

### Day 4: Finish up
```bash
# Fetch remaining episodes
python fetch_transcripts_batched.py
```

## Progress Output

```
================================================================================
Smart Batch Transcript Fetcher
================================================================================
Batch size: 50
Delay: 2s between requests
Output: flask_data/podcasts.json
================================================================================

📋 Loaded 1070 episodes from list
✓ Found 100 existing transcripts

📊 Status:
   Total episodes: 1070
   Already fetched: 100
   Need to fetch: 970
   Estimated time: ~64.7 minutes

[1/970 - 0.1%] Fetching: Understanding the True Spirit of Christmas
   ETA: 64.6m | Rate: 0.50 eps/sec | ID: IsXdO5RD_NU
   ✓ Success: 3,245 words

[2/970 - 0.2%] Fetching: Personality Psychology | Lecture One
   ETA: 64.4m | Rate: 0.48 eps/sec | ID: epoRGnCWyXw
   ✓ Success: 15,678 words

...

================================================================================
Batch checkpoint: 50/970 complete
Success: 48 | Errors: 2
Pausing 10 seconds to avoid rate limiting...
================================================================================
```

## Resume Example

**First run (interrupted):**
```bash
python fetch_transcripts_batched.py --max-episodes 50
# Fetches 30 episodes, then Ctrl+C
```

**Resume:**
```bash
python fetch_transcripts_batched.py --max-episodes 50
# Skips first 30, fetches remaining 20
```

## What Gets Saved

Each episode in `flask_data/podcasts.json`:
```json
{
  "id": "peterson-understanding-christmas",
  "title": "Understanding the True Spirit of Christmas",
  "youtube_id": "IsXdO5RD_NU",
  "guest": null,
  "url": "https://www.youtube.com/watch?v=IsXdO5RD_NU",
  "views": "50K views",
  "duration": "15:32",
  "transcript": "full text here...",
  "transcript_segments": [...],
  "transcript_status": "success",
  "fetched_at": "2026-01-08T21:45:00"
}
```

## Handling Rate Limits

If you hit YouTube's rate limit:

**Symptoms:**
```
❌ Error: Transcripts disabled or rate limited
```

**Solutions:**

1. **Wait longer** between batches
   ```bash
   python fetch_transcripts_batched.py --delay 5 --batch-size 25
   ```

2. **Smaller batches**
   ```bash
   python fetch_transcripts_batched.py --max-episodes 20
   # Wait 30 minutes
   python fetch_transcripts_batched.py --max-episodes 20
   ```

3. **Different network** (VPN, mobile hotspot, etc.)

4. **Overnight** (less competition)
   ```bash
   # Run overnight, check in morning
   nohup python fetch_transcripts_batched.py > fetch.log 2>&1 &
   ```

## Monitoring Progress

**Check how many you have:**
```bash
cat flask_data/podcasts.json | jq 'length'
```

**Count successful transcripts:**
```bash
cat flask_data/podcasts.json | jq '[.[] | select(.transcript_status == "success")] | length'
```

**See latest fetched:**
```bash
cat flask_data/podcasts.json | jq '.[0:5] | .[] | {id, title, status: .transcript_status}'
```

**Total words collected:**
```bash
cat flask_data/podcasts.json | jq '[.[] | select(.transcript != null) | .transcript | split(" ") | length] | add'
```

## Time Estimates

| Episodes | Estimated Time | Best Strategy |
|----------|---------------|---------------|
| 10       | ~1 minute     | Direct run |
| 50       | ~5 minutes    | Direct run |
| 100      | ~10 minutes   | Direct run |
| 500      | ~50 minutes   | Run in batches |
| 1,070    | ~2 hours      | Multiple sessions |

## Tips for Success

✅ **Start small** - Test with `--max-episodes 10`
✅ **Monitor rate** - Watch for errors increasing
✅ **Take breaks** - Let YouTube cool down between batches
✅ **Run overnight** - Less traffic = better success rate
✅ **Check progress** - Use `jq` to inspect results
✅ **Be patient** - 1,070 episodes takes time

## Troubleshooting

**"Episode list not found"**
```bash
python list_peterson_episodes.py
```

**All episodes showing as errors**
- Hit rate limit
- Wait 30-60 minutes
- Try different network
- Use `--delay 5` for slower requests

**Script interrupted (Ctrl+C)**
- Just run again - it resumes automatically!

**Want to re-fetch failed episodes**
- Edit `flask_data/podcasts.json` and remove error entries
- Or set `transcript_status` to null
- Run fetcher again

## Integration with Analysis

Once you have transcripts:

```bash
# Analyze first 10 episodes
./run_fresh_analysis.sh

# Check what's in your database
cat flask_data/podcasts.json | jq 'length'

# Run analysis on specific subset
# (edit analyzer to filter by date, guest, etc.)
```

## Summary

The smart batch fetcher is **the way** to get all 1,070 episodes:

1. **Checks for duplicates** - No wasted API calls
2. **Saves incrementally** - Resume anytime
3. **Rate limiting** - Avoids YouTube blocks
4. **Progress tracking** - Know how long it'll take
5. **Flexible** - Test with 10, scale to 1,070

**Start now:**
```bash
python fetch_transcripts_batched.py --max-episodes 20
```

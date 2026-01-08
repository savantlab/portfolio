# Podcast Subagent

An authenticated AI agent that queries podcast transcript data via the Flask API.

## Overview

The podcast subagent demonstrates how to:
- Authenticate with the portfolio API using bearer tokens
- Query podcast transcript data programmatically
- Search across multiple transcripts
- Analyze transcript content

## Setup

1. **Ensure API token is configured:**
   ```bash
   # Check if .env has API_TOKEN set
   grep API_TOKEN .env
   ```

2. **Install dependencies** (if not already in venv):
   ```bash
   source venv/bin/activate
   pip install requests python-dotenv
   ```

3. **Start the Flask server:**
   ```bash
   source venv/bin/activate
   python flask_driver_runner.py app:app
   ```

## Usage

The subagent has four main commands:

### 1. List all podcasts
```bash
source venv/bin/activate
python podcast_subagent.py list
```

Output shows:
- Podcast IDs and titles
- Guest names
- Publication dates
- Word counts
- YouTube URLs

### 2. Get specific podcast transcript
```bash
source venv/bin/activate
python podcast_subagent.py get peterson-thiel-2025
```

Available podcast IDs:
- `peterson-thiel-2025` - Peter Thiel (Sep 30, 2025) - 4,504 words
- `peterson-saad` - Gad Saad - 11,742 words
- `peterson-crenshaw` - Dan Crenshaw - 21,316 words
- `peterson-shapiro` - Ben Shapiro - 18,995 words

### 3. Search across all transcripts
```bash
source venv/bin/activate
python podcast_subagent.py search "feminism"
python podcast_subagent.py search "Frankfurt School"
python podcast_subagent.py search "postmodern"
```

Shows:
- Which podcasts contain the keyword
- Number of occurrences
- Context snippets around each match

### 4. Analyze transcript statistics
```bash
source venv/bin/activate
python podcast_subagent.py analyze
```

Provides:
- Total word counts
- Average words per episode
- Breakdown by guest
- Segment counts

## Authentication

The subagent automatically reads `API_TOKEN` from `.env` and includes it as a Bearer token in all requests:

```python
headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}
```

**Note:** Currently, the `/api/podcasts` endpoints are public (no auth required), but the subagent is designed to work with protected endpoints by including the bearer token in all requests.

## API Endpoints Used

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/podcasts` | GET | No | List all podcasts |
| `/api/podcasts/<id>` | GET | No | Get specific podcast |

## Example Workflow

```bash
# Terminal 1: Start Flask server
source venv/bin/activate
python flask_driver_runner.py app:app

# Terminal 2: Run subagent queries
source venv/bin/activate

# List all available podcasts
python podcast_subagent.py list

# Get the Peter Thiel episode
python podcast_subagent.py get peterson-thiel-2025

# Search for "ideology" across all transcripts
python podcast_subagent.py search ideology

# Get overall statistics
python podcast_subagent.py analyze
```

## Use Cases

### Research Analysis
Search for specific terms across all podcast transcripts to identify patterns:
```bash
python podcast_subagent.py search "cultural Marxism"
python podcast_subagent.py search "hierarchy"
python podcast_subagent.py search "chaos"
```

### Comparative Analysis
Get multiple transcripts and compare terminology:
```bash
python podcast_subagent.py get peterson-thiel-2025 > thiel.txt
python podcast_subagent.py get peterson-crenshaw > crenshaw.txt
# Then compare files with your preferred analysis tool
```

### Integration with NLP Tools
The subagent can be imported as a Python module:

```python
from podcast_subagent import PodcastSubagent

# Initialize agent
agent = PodcastSubagent()

# Get all podcasts programmatically
podcasts = agent._request('/api/podcasts')

# Process transcripts with your own NLP tools
for podcast in podcasts:
    transcript = podcast.get('transcript', '')
    # Run your analysis here...
```

## Adding More Podcasts

To add more podcast transcripts:

1. Edit `fetch_transcripts.py` and add the YouTube video ID to the `PODCASTS` list
2. Run the fetch script:
   ```bash
   source venv/bin/activate
   python fetch_transcripts.py
   ```
3. Restart Flask to reload the data

## Troubleshooting

**"API_TOKEN not found"**
- Ensure `.env` file exists and contains `API_TOKEN=your-token-here`

**"Connection refused"**
- Make sure Flask is running on port 5001
- Check with: `curl http://localhost:5001/healthz`

**Empty transcript data**
- YouTube transcripts may be disabled for some videos
- Check the `transcript_status` field in the API response

## Security Note

The API token in `.env` is NOT tracked in git (listed in `.gitignore`). Never commit your token to version control.

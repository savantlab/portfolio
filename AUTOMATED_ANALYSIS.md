# Automated Peterson Podcast Analysis

Fully automated pipeline that:
1. Fetches Peterson podcast episodes
2. Gets transcripts
3. Runs AI analysis in fresh Docker containers
4. Generates structured reports

## Architecture

```
┌──────────────────┐
│ Fetch Episodes   │  (fetch_peterson_episodes.py)
│ - YouTube IDs    │
│ - Transcripts    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Flask API        │  (Serves podcast data)
│ flask_data/      │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐     ┌──────────────────┐
│ Fresh Ollama     │◄────┤   Analyzer       │
│ (No persistence) │     │ (Automated AI)   │
└──────────────────┘     └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │ analysis_output/ │
                         │ - JSON results   │
                         │ - Markdown report│
                         └──────────────────┘
```

## Quick Start

### One Command
```bash
./run_fresh_analysis.sh
```

This will:
1. Start fresh Ollama container (no persistent storage)
2. Start Flask API with podcast data
3. Pull gemma3:latest model
4. Run automated analysis on all episodes
5. Save results to `analysis_output/`
6. Ask if you want to clean up containers

### With Episode Refresh
```bash
./run_fresh_analysis.sh --fetch
```

Fetches latest episodes before analysis.

## Manual Workflow

### 1. Fetch Episodes
```bash
source venv/bin/activate
python fetch_peterson_episodes.py
```

### 2. Run Analysis Pipeline
```bash
docker-compose -f docker-compose.fresh.yml up
```

### 3. View Results
```bash
ls -lh analysis_output/
cat analysis_output/report_*.md
```

## What Gets Analyzed

For each podcast episode, the analyzer runs 4 types of analysis:

1. **Themes** - Main topics and themes discussed
2. **Ideology** - Ideological framework and worldview
3. **Rhetoric** - Persuasive techniques and strategies
4. **Terminology** - Key terms and language patterns

## Output Files

### JSON Results (`analysis_YYYYMMDD_HHMMSS.json`)
```json
[
  {
    "podcast_id": "peterson-peter-thiel",
    "title": "Jordan Peterson & Peter Thiel",
    "guest": "Peter Thiel",
    "analysis_type": "themes",
    "analysis": "...",
    "transcript_length": 45000,
    "timestamp": "2026-01-08T21:00:00"
  },
  ...
]
```

### Markdown Report (`report_YYYYMMDD_HHMMSS.md`)
Human-readable report organized by episode and analysis type.

## Configuration

### Environment Variables
Create/edit `.env`:
```bash
API_TOKEN=your-token-here
OLLAMA_MODEL=gemma3:latest
```

### Choose Different Model
Edit `docker-compose.fresh.yml`:
```yaml
environment:
  - OLLAMA_MODEL=mistral:7b  # or llama3.2:3b, etc.
```

### Adjust Analysis Types
Edit `peterson_analyzer.py`, line 188:
```python
analysis_types = ["themes", "ideology", "rhetoric", "terminology"]
# Add more: "sentiment", "comparisons", etc.
```

## Why "Fresh" Ollama?

**No Persistent Storage** = Clean slate every time

Benefits:
- Reproducible results
- No model drift
- No cached responses
- Consistent baseline
- Easier debugging

How it works:
- Regular Ollama: Uses Docker volume (`ollama_data`)
- Fresh Ollama: No volume mount = starts empty
- Each run pulls model fresh
- Analysis runs on clean model
- Container deleted after = truly fresh next time

## Advanced Usage

### Analyze Specific Episodes Only

1. Edit `fetch_peterson_episodes.py` line 43:
```python
known_episodes = [
    ("urk9BJIxZ3U", "Jordan Peterson & Peter Thiel", "Peter Thiel", "2025-09-30"),
    # Add/remove episodes here
]
```

2. Run:
```bash
python fetch_peterson_episodes.py
./run_fresh_analysis.sh
```

### Use Different Ollama Models

```bash
# Edit docker-compose.fresh.yml
environment:
  - OLLAMA_MODEL=llama3.1:70b  # Larger, more capable

# Or set in terminal
export OLLAMA_MODEL=mistral:7b
./run_fresh_analysis.sh
```

### Run Analyzer Without Docker

```bash
# Terminal 1: Start Ollama locally
ollama serve

# Terminal 2: Start Flask
source venv/bin/activate
python flask_driver_runner.py app:app

# Terminal 3: Run analyzer
source venv/bin/activate
export FLASK_URL=http://localhost:5001
export OLLAMA_URL=http://localhost:11434
export OUTPUT_DIR=./analysis_output
python peterson_analyzer.py
```

### Add Custom Analysis Types

Edit `peterson_analyzer.py`, method `analyze_episode()`:

```python
queries = {
    "themes": "...",
    "ideology": "...",
    "rhetoric": "...",
    "terminology": "...",
    "sentiment": "Analyze the emotional tone and sentiment in this excerpt.",
    "comparisons": "Compare this to typical academic discourse. What differs?",
    "fallacies": "Identify logical fallacies or rhetorical weaknesses.",
}
```

Then update line 188:
```python
analysis_types = ["themes", "ideology", "rhetoric", "terminology", "sentiment", "fallacies"]
```

## Troubleshooting

### "Docker daemon not running"
```bash
# Start Docker Desktop
open -a Docker
```

### "Port already in use"
```bash
# Check what's using port 11435
lsof -ti:11435 | xargs kill

# Or use different port in docker-compose.fresh.yml
ports:
  - "11436:11434"
```

### "Model pull failed"
- Check internet connection
- Try smaller model: `OLLAMA_MODEL=gemma3:latest`
- Check Docker has enough disk space

### "Analysis timeout"
- Increase timeout in `peterson_analyzer.py` line 112:
```python
timeout=300  # 5 minutes
```

### "Out of memory"
- Use smaller model: `gemma3:latest` (3.3GB)
- Reduce concurrent processing
- Increase Docker memory limit

## Performance

### Speed Estimates (gemma3:latest)

| Episodes | Analysis Time | Output Size |
|----------|---------------|-------------|
| 4        | ~10 minutes   | ~50 KB JSON |
| 10       | ~25 minutes   | ~125 KB JSON|
| 50       | ~2 hours      | ~600 KB JSON|

*Times include model download on fresh Ollama*

### Resource Usage

| Model | RAM | Disk | Speed |
|-------|-----|------|-------|
| gemma3:latest | 4-8 GB | 3.3 GB | Fast |
| mistral:7b | 8-12 GB | 7 GB | Medium |
| llama3.1:70b | 48+ GB | 70 GB | Slow |

## Integration with Research Workflow

### Export for Further Analysis
```bash
# Convert JSON to CSV for Excel/Pandas
cat analysis_output/analysis_*.json | \
  jq -r '.[] | [.podcast_id, .analysis_type, .analysis] | @csv' > results.csv
```

### Compare Analyses
```bash
# Run analysis twice with different models
OLLAMA_MODEL=gemma3:latest ./run_fresh_analysis.sh
mv analysis_output/analysis_*.json gemma_results.json

OLLAMA_MODEL=mistral:7b ./run_fresh_analysis.sh
mv analysis_output/analysis_*.json mistral_results.json

# Compare results
diff gemma_results.json mistral_results.json
```

### Scheduled Runs
Add to crontab:
```bash
# Run analysis daily at 2 AM
0 2 * * * cd /path/to/savantlab-portfolio && ./run_fresh_analysis.sh --fetch
```

## Cleanup

### Remove All Analysis Data
```bash
rm -rf analysis_output/
```

### Remove Docker Images
```bash
docker-compose -f docker-compose.fresh.yml down --rmi all
```

### Full Reset
```bash
docker-compose -f docker-compose.fresh.yml down --volumes --rmi all
rm -rf analysis_output/
```

## Next Steps

### Extend the Analyzer
- Add comparative analysis across episodes
- Implement vector embeddings for semantic search
- Generate network graphs of concepts
- Track terminology evolution over time

### Integrate with Your Research
- Export to LaTeX for papers
- Generate visualizations
- Cross-reference with other Peterson content
- Compare with other public figures

## Files Reference

| File | Purpose |
|------|---------|
| `fetch_peterson_episodes.py` | Fetch episodes and transcripts |
| `peterson_analyzer.py` | Automated analysis engine |
| `docker-compose.fresh.yml` | Fresh Ollama + services |
| `Dockerfile.analyzer` | Container for analyzer |
| `run_fresh_analysis.sh` | One-command pipeline |
| `analysis_output/` | Results directory |

## Support

For issues or questions:
1. Check troubleshooting section
2. Review Docker logs: `docker-compose -f docker-compose.fresh.yml logs`
3. Check analyzer logs: `docker logs peterson-analyzer`

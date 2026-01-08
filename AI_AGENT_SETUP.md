# Podcast AI Agent Setup

Interactive AI agent using **Ollama** (open-source LLM) to discuss and analyze podcast transcripts.

## Overview

This setup provides:
- **Open-source LLM** via Ollama (runs locally, no cloud APIs)
- **Interactive chat interface** to discuss podcast content
- **Automatic context injection** from your Flask API
- **Docker deployment** option for isolated environment

## Quick Start (Local)

### Prerequisites
- Ollama installed and running
- Flask API running
- Python 3.11+ with venv

### 1. Start Ollama (if not running)
```bash
# Check if running
curl http://localhost:11434/api/tags

# If not running, start it
ollama serve
```

### 2. Pull a model (if needed)
```bash
# You already have these models:
ollama list

# Or pull a new one
ollama pull llama3.2:3b     # Smaller, faster
ollama pull mistral:7b      # Good balance
ollama pull llama3.1:70b    # More capable (requires more RAM)
```

### 3. Start Flask API
```bash
# Terminal 1
source venv/bin/activate
python flask_driver_runner.py app:app
```

### 4. Run the AI Agent
```bash
# Terminal 2
source venv/bin/activate
python podcast_ai_agent.py

# Or specify a different model
python podcast_ai_agent.py --model gemma3:latest
```

## Usage Examples

Once the agent starts, you'll see:
```
================================================================================
🎙️  Podcast AI Agent - Interactive Mode
================================================================================
Model: gemma3:latest
Flask API: http://localhost:5001
Ollama API: http://localhost:11434

✓ Loaded 4 podcasts
```

### Example Interactions

**List available podcasts:**
```
🤔 You: list
```

**Ask about specific content:**
```
🤔 You: What does Peter Thiel discuss in his episode?
🤔 You: How many times does Peterson mention "hierarchy" in the Crenshaw episode?
🤔 You: Summarize the main themes in the Ben Shapiro podcast
```

**Search across transcripts:**
```
🤔 You: search feminism
🤔 You: search Frankfurt School
```

**Load specific podcast for deeper context:**
```
🤔 You: load peterson-thiel-2025
🤔 You: What does Thiel say about technology?
```

**Comparative analysis:**
```
🤔 You: Compare how Peterson talks about ideology with Thiel vs Shapiro
🤔 You: What themes appear in all four podcasts?
```

**Exit:**
```
🤔 You: quit
```

## Docker Deployment

For a fully containerized setup:

### 1. Build and start all services
```bash
docker-compose -f docker-compose.agent.yml up -d
```

This starts:
- **Ollama** container (LLM inference)
- **Flask** container (API with podcast data)
- **Agent** container (AI agent)

### 2. Download a model into Ollama container
```bash
docker exec -it podcast-ollama ollama pull gemma3:latest
```

### 3. Attach to the agent
```bash
docker attach podcast-agent
```

### 4. Stop services
```bash
docker-compose -f docker-compose.agent.yml down
```

## Available Models

Your current models:
- `gemma3:latest` (3.3 GB) - Fast, efficient
- `gpt-oss:20b` (13 GB) - More capable
- `glm-4.6:cloud` - Cloud-based variant

Recommended models for this task:
- **gemma3:latest** - Best balance (default)
- **llama3.2:3b** - Fastest, good for quick queries
- **mistral:7b** - Good reasoning capabilities
- **mixtral:8x7b** - Best quality (requires more RAM)

## Customization

### Change model at runtime
```bash
python podcast_ai_agent.py --model mistral:7b
```

### Point to different Flask instance
```bash
python podcast_ai_agent.py --api-url http://192.168.1.100:5001
```

### Use remote Ollama server
```bash
python podcast_ai_agent.py --ollama-url http://remote-server:11434
```

## Advanced: Programmatic Usage

You can also import and use the agent in your own scripts:

```python
from podcast_ai_agent import PodcastAIAgent

# Initialize
agent = PodcastAIAgent(
    flask_url="http://localhost:5001",
    ollama_url="http://localhost:11434",
    model="gemma3:latest"
)

# Load data
agent.load_podcasts()

# Query programmatically
response = agent.process_query("What are the main themes?")
print(response)

# Search
results = agent.search_podcasts("ideology")
for r in results:
    print(f"{r['podcast']['title']}: {r['count']} occurrences")
```

## Architecture

```
┌─────────────────┐
│   You (User)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│   AI Agent      │─────▶│  Flask API       │
│  (Python CLI)   │      │  (Podcast Data)  │
└────────┬────────┘      └──────────────────┘
         │
         ▼
┌─────────────────┐
│     Ollama      │
│  (LLM Engine)   │
└─────────────────┘
```

**Flow:**
1. You ask a question
2. Agent fetches relevant podcast data from Flask API
3. Agent builds context + question prompt
4. Agent sends to Ollama for inference
5. Agent returns answer to you

## Performance Tips

### For faster responses:
- Use smaller models (`gemma3`, `llama3.2:3b`)
- Reduce context size (modify `build_context()` method)
- Use GPU acceleration if available (Ollama auto-detects)

### For better quality:
- Use larger models (`mixtral`, `llama3.1:70b`)
- Load specific podcasts with `load <podcast_id>` for focused context
- Ask more specific questions

## Troubleshooting

**"Ollama is not running"**
```bash
ollama serve &
```

**"Flask API is not running"**
```bash
source venv/bin/activate
python flask_driver_runner.py app:app
```

**Slow responses:**
- Model might be too large for your hardware
- Try smaller model: `python podcast_ai_agent.py --model gemma3:latest`
- Check CPU/RAM usage

**Out of memory:**
- Use smaller model
- Reduce context by not loading full transcripts

**Connection timeout:**
- Increase timeout in `query_ollama()` method
- Check Ollama is running: `curl http://localhost:11434/api/tags`

## Security Notes

- API tokens are loaded from `.env` (not tracked in git)
- All processing happens locally (no external API calls)
- Ollama runs entirely on your machine
- Docker containers are isolated from host system

## Next Steps

### Integrate with your research workflow:
1. Export conversations for documentation
2. Build automated analysis pipelines
3. Generate reports from transcript analysis
4. Create vector embeddings for semantic search

### Extend the agent:
- Add RAG (Retrieval-Augmented Generation)
- Implement conversation memory
- Add export functions (CSV, JSON, Markdown)
- Create specialized analysis modes (rhetoric, ideology, etc.)

## Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [Ollama Models Library](https://ollama.ai/library)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [Ollama Docker](https://hub.docker.com/r/ollama/ollama)

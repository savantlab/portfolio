# Agent Comparison

Two tools for working with podcast transcript data:

## 1. Basic Subagent (`podcast_subagent.py`)

**Purpose:** Programmatic access to podcast data

**Use when:**
- You need structured data output
- Building automation/scripts
- Quick keyword searches
- Generating reports

**Features:**
- ✓ List all podcasts
- ✓ Get specific transcripts
- ✓ Search for keywords
- ✓ Generate statistics
- ✓ No AI/LLM required
- ✓ Fast, deterministic results

**Example:**
```bash
python podcast_subagent.py list
python podcast_subagent.py search "ideology"
python podcast_subagent.py analyze
```

**Output:** Structured text, JSON-like data

---

## 2. AI Agent (`podcast_ai_agent.py`)

**Purpose:** Natural language discussion and analysis

**Use when:**
- You want to ask questions in plain English
- Need summaries or explanations
- Want comparative analysis
- Exploring themes and patterns

**Features:**
- ✓ Natural language interface
- ✓ Context-aware responses
- ✓ Summarization
- ✓ Theme extraction
- ✓ Comparative analysis
- ✓ Follow-up questions
- ✗ Requires Ollama/LLM
- ✗ Slower than basic subagent

**Example:**
```bash
python podcast_ai_agent.py

🤔 You: What are the main themes in the Peter Thiel episode?
🤖 AI: [Natural language response based on transcript]

🤔 You: How does that compare to the Shapiro episode?
🤖 AI: [Comparative analysis]
```

**Output:** Natural language responses, conversational

---

## Comparison Table

| Feature | Basic Subagent | AI Agent |
|---------|---------------|----------|
| Speed | ⚡ Fast | 🐌 Slower |
| Setup | Simple | Requires Ollama |
| Output | Structured data | Natural language |
| Questions | Commands only | Natural language |
| Analysis | Keyword counts | Thematic understanding |
| Memory | None | Conversation context |
| API calls | Flask only | Flask + Ollama |
| Offline | ✓ Yes | ✓ Yes (with Ollama) |
| Resource usage | Low | Medium-High |

---

## When to Use Each

### Use Basic Subagent for:
1. **Quick searches:** "Does Peterson mention X?"
2. **Data extraction:** Export transcripts, count occurrences
3. **Automation:** Scripting, batch processing
4. **Fast results:** No LLM inference overhead
5. **CI/CD pipelines:** Deterministic results

### Use AI Agent for:
1. **Research questions:** "What is Peterson's view on...?"
2. **Summaries:** "Summarize the main arguments in..."
3. **Comparisons:** "How does X differ from Y?"
4. **Theme extraction:** "What are common themes?"
5. **Interactive exploration:** Follow-up questions

---

## Example Workflows

### Workflow 1: Quick Data Check
```bash
# Use basic subagent
python podcast_subagent.py search "Frankfurt School"
python podcast_subagent.py get peterson-thiel-2025
```

### Workflow 2: Research Analysis
```bash
# Use AI agent
python podcast_ai_agent.py

🤔 You: What are the main ideological themes across all episodes?
🤔 You: How does Peterson frame cultural issues?
🤔 You: Compare Peterson's rhetoric with Thiel vs Shapiro
```

### Workflow 3: Combined Approach
```bash
# Step 1: Use basic subagent to find relevant content
python podcast_subagent.py search "postmodern"
# Output: Found in 3 podcasts

# Step 2: Use AI agent for deeper analysis
python podcast_ai_agent.py
🤔 You: load peterson-shapiro
🤔 You: Analyze how Peterson uses "postmodern" in this episode
```

---

## Technical Details

### Basic Subagent
- **Language:** Python 3.11+
- **Dependencies:** requests, python-dotenv
- **API:** Flask REST API
- **Response time:** <100ms
- **Memory:** ~50MB

### AI Agent
- **Language:** Python 3.11+
- **Dependencies:** requests, python-dotenv
- **APIs:** Flask REST + Ollama
- **Response time:** 2-30s (depends on model)
- **Memory:** 500MB - 8GB (depends on model)
- **LLM:** Any Ollama model (gemma3, llama3, mistral, etc.)

---

## Integration

Both agents can be used together or independently:

```python
# In your own Python script
from podcast_subagent import PodcastSubagent
from podcast_ai_agent import PodcastAIAgent

# Quick data check
basic = PodcastSubagent()
results = basic.search_transcripts("ideology")

# Deep analysis on results
if results:
    ai = PodcastAIAgent()
    ai.load_podcasts()
    response = ai.process_query(f"Analyze ideology mentions in {results[0]['podcast']['title']}")
    print(response)
```

---

## Which Should I Use?

**Start with the basic subagent** to:
- Explore the data
- Find relevant content
- Get quick answers

**Switch to the AI agent** when:
- You need natural language explanations
- Want to explore themes and patterns
- Need comparative analysis
- Have open-ended research questions

**Use both** for comprehensive research workflows!

#!/bin/bash

# Quick start script for Podcast AI Agent

echo "🚀 Starting Podcast AI Agent..."
echo ""

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama is not running"
    echo "   Start it with: ollama serve"
    exit 1
fi
echo "✓ Ollama is running"

# Check if Flask is running
if ! curl -s http://localhost:5001/healthz > /dev/null 2>&1; then
    echo "❌ Flask API is not running"
    echo "   Start it in another terminal with:"
    echo "   source venv/bin/activate"
    echo "   python flask_driver_runner.py app:app"
    exit 1
fi
echo "✓ Flask API is running"

# Activate virtual environment and run agent
echo "✓ Starting AI agent..."
echo ""

source venv/bin/activate
python podcast_ai_agent.py "$@"

#!/bin/bash

# Run Fresh Peterson Analysis Pipeline
# This script:
# 1. Fetches latest episodes (optional)
# 2. Starts fresh Ollama + Flask + Analyzer in Docker
# 3. Runs automated analysis
# 4. Saves results to analysis_output/
# 5. Tears down containers (Ollama starts fresh next time)

set -e

echo "="
echo "Peterson Podcast Analysis Pipeline"
echo "="
echo ""

# Step 1: Fetch episodes (optional)
if [ "$1" == "--fetch" ]; then
    echo "📥 Fetching latest Peterson episodes..."
    source venv/bin/activate
    python fetch_peterson_episodes.py
    echo "✓ Episodes updated"
    echo ""
fi

# Step 2: Ensure output directory exists
mkdir -p analysis_output

# Step 3: Stop any existing containers
echo "🧹 Cleaning up old containers..."
docker-compose -f docker-compose.fresh.yml down 2>/dev/null || true
echo ""

# Step 4: Build and start services
echo "🚀 Starting services..."
docker-compose -f docker-compose.fresh.yml build
docker-compose -f docker-compose.fresh.yml up -d ollama-fresh flask
echo ""

# Step 5: Wait for services to be ready
echo "⏳ Waiting for services..."
sleep 10

# Check Flask health
until curl -s http://localhost:5002/healthz > /dev/null 2>&1; do
    echo "  Waiting for Flask..."
    sleep 2
done
echo "✓ Flask ready"

# Check Ollama health
until curl -s http://localhost:11435/api/tags > /dev/null 2>&1; do
    echo "  Waiting for Ollama..."
    sleep 5
done
echo "✓ Ollama ready"
echo ""

# Step 6: Run analyzer
echo "🤖 Running analysis..."
docker-compose -f docker-compose.fresh.yml up analyzer

# Step 7: Show results
echo ""
echo "="
echo "✓ Analysis Complete"
echo "="
echo ""
echo "Results saved to: analysis_output/"
ls -lh analysis_output/ | tail -5
echo ""

# Step 8: Cleanup (optional)
read -p "Clean up containers? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧹 Cleaning up..."
    docker-compose -f docker-compose.fresh.yml down
    echo "✓ Containers removed"
fi

echo ""
echo "Done!"

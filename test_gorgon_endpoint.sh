#!/bin/bash

# Test the password-protected Gorgon endpoint

echo "=========================================="
echo "Testing /gorgon/peterson-podcasts.json"
echo "=========================================="
echo ""

# Test 1: No password (should fail)
echo "Test 1: No password (should fail)"
echo "Command: curl http://localhost:5001/gorgon/peterson-podcasts.json"
curl -s http://localhost:5001/gorgon/peterson-podcasts.json | jq
echo ""
echo "=========================================="
echo ""

# Test 2: Wrong password (should fail)
echo "Test 2: Wrong password (should fail)"
echo "Command: curl http://localhost:5001/gorgon/peterson-podcasts.json?password=WRONG"
curl -s "http://localhost:5001/gorgon/peterson-podcasts.json?password=WRONG" | jq
echo ""
echo "=========================================="
echo ""

# Test 3: Correct password via query param (should succeed)
echo "Test 3: Correct password via query param (should succeed)"
echo "Command: curl http://localhost:5001/gorgon/peterson-podcasts.json?password=ARCHIMEDES2026"
curl -s "http://localhost:5001/gorgon/peterson-podcasts.json?password=ARCHIMEDES2026" | jq '{project, description, total_episodes, episode_sample: .episodes[0:2]}'
echo ""
echo "=========================================="
echo ""

# Test 4: Correct password via header (should succeed)
echo "Test 4: Correct password via header (should succeed)"
echo "Command: curl -H 'X-Gorgon-Password: ARCHIMEDES2026' http://localhost:5001/gorgon/peterson-podcasts.json"
curl -s -H "X-Gorgon-Password: ARCHIMEDES2026" http://localhost:5001/gorgon/peterson-podcasts.json | jq '{project, description, total_episodes, episode_sample: .episodes[0:2]}'
echo ""
echo "=========================================="
echo ""

echo "✓ Tests complete!"
echo ""
echo "Usage examples:"
echo "  Query param:  curl 'http://localhost:5001/gorgon/peterson-podcasts.json?password=ARCHIMEDES2026'"
echo "  Header:       curl -H 'X-Gorgon-Password: ARCHIMEDES2026' http://localhost:5001/gorgon/peterson-podcasts.json"
echo "  Production:   curl 'https://savantlab.org/gorgon/peterson-podcasts.json?password=ARCHIMEDES2026'"

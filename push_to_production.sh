#!/bin/bash
# Push enriched project data to production

API_TOKEN="${API_TOKEN:-LGAhPDfdAgjozkNP2YrDLb_txhydOa1pv0fsdix16EQ}"

echo "Pushing enriched project data to production..."
curl -X POST https://savantlab.org/api/projects/populate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d @flask_data/projects.json

echo -e "\n\nDone! Check https://savantlab.org"

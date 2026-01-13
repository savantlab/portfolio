#!/bin/bash
# Push enriched project data to production

: "${API_TOKEN:?Set API_TOKEN in your environment}"

echo "Pushing enriched project data to production..."
curl -X POST https://savantlab.org/api/projects/populate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d @flask_data/projects.json

echo -e "\n\nDone! Check https://savantlab.org"

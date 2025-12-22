#!/bin/bash

# Deployment Helper Script
# Automates the deployment process with proper checks

set -e  # Exit on error

echo "========================================="
echo "Portfolio Deployment Helper"
echo "========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo -e "${RED}ERROR: You must be on the main branch${NC}"
    echo "Current branch: $CURRENT_BRANCH"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${RED}ERROR: You have uncommitted changes${NC}"
    echo "Please commit or stash your changes first"
    git status
    exit 1
fi

echo -e "${GREEN}✓ On main branch with clean working directory${NC}"
echo ""

# Pull latest main
echo "Pulling latest changes from main..."
git pull origin main
echo -e "${GREEN}✓ Main branch up to date${NC}"
echo ""

# Run local tests
echo "Running local validation tests..."
echo ""

echo "1. Testing Flask app imports..."
if python3 -c "from app import app, PROJECTS, PUBLICATIONS; print('✓ Flask app imports successfully')"; then
    echo -e "${GREEN}✓ Flask imports OK${NC}"
else
    echo -e "${RED}✗ Flask imports FAILED${NC}"
    exit 1
fi
echo ""

echo "2. Validating data structures..."
if python3 -c "
from app import PROJECTS, PUBLICATIONS
import sys

# Validate PROJECTS
required_keys = ['id', 'title', 'subtitle', 'description', 'tech', 'highlights', 'github', 'status', 'image']
for p in PROJECTS:
    for k in required_keys:
        if k not in p:
            print(f'ERROR: Project {p.get(\"id\", \"unknown\")} missing key: {k}')
            sys.exit(1)

# Validate PUBLICATIONS  
for pub in PUBLICATIONS:
    for k in ['title', 'status', 'description']:
        if k not in pub:
            print(f'ERROR: Publication missing key: {k}')
            sys.exit(1)

print('✓ All data structures valid')
"; then
    echo -e "${GREEN}✓ Data validation OK${NC}"
else
    echo -e "${RED}✗ Data validation FAILED${NC}"
    exit 1
fi
echo ""

echo "3. Testing Flask routes..."
if python3 -c "
from app import app, PROJECTS
import sys

with app.test_client() as client:
    for route in ['/', '/about', '/contact', '/journal', '/counterterrorism', '/healthz']:
        r = client.get(route)
        if r.status_code not in [200, 404]:
            print(f'ERROR: Route {route} failed')
            sys.exit(1)
    
    for p in PROJECTS:
        r = client.get(f'/project/{p[\"id\"]}')
        if r.status_code != 200:
            print(f'ERROR: Project route failed: {p[\"id\"]}')
            sys.exit(1)

print('✓ All routes working')
"; then
    echo -e "${GREEN}✓ Route testing OK${NC}"
else
    echo -e "${RED}✗ Route testing FAILED${NC}"
    exit 1
fi
echo ""

echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}All local tests passed!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""

# Show diff between main and deploy
echo "Comparing main vs deploy branch..."
git fetch origin deploy
echo ""
echo "Changes to be deployed:"
echo "----------------------------------------"
git --no-pager log origin/deploy..HEAD --oneline
echo "----------------------------------------"
echo ""

# Confirmation prompt
echo -e "${YELLOW}Ready to deploy these changes to production?${NC}"
echo "This will:"
echo "1. Checkout deploy branch"
echo "2. Merge main into deploy"
echo "3. Push to trigger deployment"
echo ""
read -p "Continue? (yes/no): " -r
echo ""

if [[ ! $REPLY =~ ^[Yy]es$ ]]; then
    echo "Deployment cancelled"
    exit 0
fi

# Deploy
echo "Deploying..."
echo ""

git checkout deploy
git pull origin deploy
git merge main -m "Deploy: Merge main into deploy

Co-Authored-By: Warp <agent@warp.dev>"

# Add JSON data files (not in main branch)
if [ -d "data" ]; then
    echo "Adding data files to deploy branch..."
    git add -f data/*.json 2>/dev/null || true
    if ! git diff --cached --quiet; then
        git commit -m "Update data files for deployment

Co-Authored-By: Warp <agent@warp.dev>"
    fi
fi

git push origin deploy

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}Deployment triggered successfully!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "Monitor deployment at:"
echo "https://github.com/savantlab/portfolio/actions"
echo ""
echo "After deployment completes, verify at:"
echo "https://savantlab.org"
echo ""

# Return to main branch
git checkout main
echo -e "${GREEN}Returned to main branch${NC}"

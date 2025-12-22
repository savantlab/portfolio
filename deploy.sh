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

# Temporarily copy data from deploy branch for testing
echo "Setting up test environment..."
git fetch origin deploy
if ! git show origin/deploy:data/ > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠ No data directory on deploy branch, skipping tests${NC}"
else
    # Extract data directory from deploy branch
    git archive origin/deploy data/ | tar -x
    echo -e "${GREEN}✓ Test data loaded from deploy branch${NC}"
fi
echo ""

# Run local tests
echo "Running test suite..."
echo ""

echo "1. Running pytest..."
if pytest tests/ -v --tb=short --no-cov; then
    echo -e "${GREEN}✓ All tests passed${NC}"
else
    echo -e "${RED}✗ Tests FAILED${NC}"
    echo ""
    echo "To see detailed test results, run: pytest tests/ -v"
    exit 1
fi
echo ""

echo "2. Running code quality checks..."
if flake8 app.py contact_list.py --count --select=E9,F63,F7,F82 --show-source --statistics > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Code quality checks passed${NC}"
else
    echo -e "${YELLOW}⚠ Code quality warnings (non-blocking)${NC}"
fi
echo ""

echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}All local tests passed!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""

# Backup local data directory if it exists
LOCAL_DATA_EXISTS=false
if [ -d "data" ] && [ -n "$(ls -A data 2>/dev/null)" ]; then
    LOCAL_DATA_EXISTS=true
    echo "Backing up local data directory..."
    mv data data_backup
    echo -e "${GREEN}✓ Local data backed up${NC}"
    echo ""
fi

# Clean up test data from deploy branch
if [ -d "data" ]; then
    echo "Cleaning up test data..."
    rm -rf data/
    echo -e "${GREEN}✓ Test data cleaned up${NC}"
    echo ""
fi

# Restore local data directory
if [ "$LOCAL_DATA_EXISTS" = true ]; then
    echo "Restoring local data directory..."
    mv data_backup data
    echo -e "${GREEN}✓ Local data restored${NC}"
    echo ""
fi

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

# Validate and add JSON data files (not in main branch)
if [ -d "data" ]; then
    echo "Validating JSON data files..."
    
    # Validate each JSON file
    json_valid=true
    for json_file in data/*.json; do
        if [ -f "$json_file" ]; then
            echo "  Checking $json_file..."
            if python3 -m json.tool "$json_file" > /dev/null 2>&1; then
                echo -e "  ${GREEN}✓ Valid JSON${NC}"
            else
                echo -e "  ${RED}✗ Invalid JSON: $json_file${NC}"
                json_valid=false
            fi
        fi
    done
    
    if [ "$json_valid" = false ]; then
        echo -e "${RED}ERROR: Invalid JSON files detected${NC}"
        echo "Please fix JSON syntax errors before deploying"
        git checkout main
        exit 1
    fi
    
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

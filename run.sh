#!/bin/bash

# Savantlab Portfolio - Automated Startup Script
# Handles authentication and starts Flask app with chromedriver

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
EMAIL="stephie.maths@icloud.com"
API_URL="${API_URL:-http://localhost:5001}"
VENV_PATH="venv"

# Helper functions
print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

# Check if virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    print_error "Virtual environment not found at $VENV_PATH"
    print_info "Please create it with: python -m venv venv"
    exit 1
fi

# Activate virtual environment
source "$VENV_PATH/bin/activate"
print_success "Virtual environment activated"

# Check if required Python packages are installed
print_info "Checking dependencies..."
python -c "import flask, selenium, requests" 2>/dev/null || {
    print_error "Missing dependencies"
    print_info "Installing dependencies..."
    pip install -q -r requirements.txt
    print_success "Dependencies installed"
}

# Function to request and verify token
setup_auth() {
    print_header "Setting Up Authentication"
    
    print_info "Requesting authentication token for $EMAIL..."
    
    # Request token via API
    TOKEN_RESPONSE=$(curl -s -X POST "$API_URL/api/auth/token" \
        -H "Content-Type: application/json" \
        -d "{\"email\": \"$EMAIL\"}" 2>/dev/null)
    
    # Extract token from response
    TOKEN=$(echo "$TOKEN_RESPONSE" | python -c "import sys, json; data=json.load(sys.stdin); print(data.get('token', ''))" 2>/dev/null)
    
    if [ -z "$TOKEN" ]; then
        print_error "Failed to obtain authentication token"
        print_info "Make sure the Flask app is running"
        return 1
    fi
    
    print_success "Token obtained: ${TOKEN:0:20}..."
    
    # Verify token
    print_info "Verifying token..."
    VERIFY_RESPONSE=$(curl -s -X POST "$API_URL/api/auth/verify" \
        -H "Content-Type: application/json" \
        -d "{\"token\": \"$TOKEN\"}" 2>/dev/null)
    
    if echo "$VERIFY_RESPONSE" | grep -q '"success"'; then
        print_success "Token verified"
        
        # Export token for use
        export API_TOKEN="$TOKEN"
        
        # Save token to environment file for reference
        echo "export API_TOKEN=\"$TOKEN\"" > .env.token
        print_info "Token saved to .env.token for manual use"
        
        return 0
    else
        print_error "Token verification failed"
        return 1
    fi
}

# Main startup process
main() {
    print_header "Savantlab Portfolio - Starting"
    
    # Start Flask app in background
    print_info "Starting Flask app with chromedriver..."
    
    # Start flask_driver_runner in background
    python flask_driver_runner.py app:app &
    FLASK_PID=$!
    
    print_success "Flask app started (PID: $FLASK_PID)"
    
    # Wait for Flask to start
    print_info "Waiting for Flask app to be ready..."
    sleep 3
    
    # Check if Flask is actually running
    if ! kill -0 $FLASK_PID 2>/dev/null; then
        print_error "Flask app failed to start"
        exit 1
    fi
    
    # Setup authentication
    setup_auth
    AUTH_RESULT=$?
    
    if [ $AUTH_RESULT -eq 0 ]; then
        print_header "Application Ready"
        print_success "API is authenticated and ready"
        print_info "Chrome should open at http://localhost:5001"
        print_info "Visit http://localhost:5001/reading to see your reading list"
        echo ""
        print_info "To add items from another terminal, use:"
        echo "  python reading_list_cli.py list"
        echo "  python reading_list_cli.py add \"Title\" --category Research"
        echo ""
        print_info "Press Ctrl+C to stop the app"
    else
        print_error "Authentication setup failed"
        print_info "The Flask app is running but not authenticated"
        print_info "You can still use it by running the CLI commands manually"
    fi
    
    # Wait for Flask process to complete (until interrupted)
    wait $FLASK_PID
}

# Trap exit to clean up
cleanup() {
    print_info "Shutting down..."
    # Kill any remaining Flask processes
    pkill -P $$ 2>/dev/null || true
    exit 0
}

trap cleanup EXIT INT TERM

# Run main function
main

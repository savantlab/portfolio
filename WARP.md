# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Core Development Commands

### Virtual Environment
Always activate the virtual environment before running commands:
```bash
source venv/bin/activate
```

### Running the Application
```bash
# Recommended: Flask with Chromedriver lifecycle management
# (auto-shutdown when browser closes)
python flask_driver_runner.py app:app
python flask_driver_runner.py app:app --headless
python flask_driver_runner.py app:app --port 5002

# Alternative: Standard Flask development server (when browser automation not needed)
python app.py
```

**Note**: You can run both Jupyter and Flask driver simultaneously in the same Chrome/Chromedriver session.

### Production Deployment
```bash
# Production server with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Testing and Validation
```bash
# Run all tests with pytest
pytest

# Run tests with verbose output
pytest -v

# Run tests with coverage report
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_app.py

# Run specific test class
pytest tests/test_app.py::TestWebRoutes

# Run specific test
pytest tests/test_app.py::TestWebRoutes::test_homepage

# Run code quality checks
flake8 app.py contact_list.py
black --check .

# Run comprehensive deployment validation (includes tests)
./deploy.sh
```

## Architecture Overview

### Data-Driven Architecture
The portfolio uses **JSON files as the data source** loaded at application startup:
- `data/projects.json` - Project showcase data
- `data/publications.json` - Publication listings  
- `data/about.json` - About page content
- `data/contact.json` - Contact page content
- `data/contact_*.json` - Contact microservice endpoints (research, speaking, consulting, collaboration)

These JSON files are loaded via `load_json_data()` in `app.py` and injected into global variables (`PROJECTS`, `PUBLICATIONS`, etc.).

### Contact Microservices: Linked List Architecture
The contact system uses a **custom linked list implementation** (`contact_list.py`) to manage contact microservices:
- Each microservice (research, speaking, consulting, collaboration) is a node with `service_id`, `endpoint`, and `data`
- Linked list pattern enables navigation between contact pages (previous/next)
- API endpoints: `/api/contact/list`, `/api/contact/add` for programmatic access
- Web routes: `/contact/<service_id>` for individual service pages

**Key insight**: This is not just data storage—it's a traversable data structure demonstrating computer science fundamentals in a real application.

### Database Models (Unused in Current App)
The codebase contains SQLAlchemy models (`models.py`, `database.py`, `blog.py`, `projects.py`, `technical_implementation.py`) that are **NOT currently active** in the main application. These provide:
- `BlogPost` - Blog post management with tags
- `Project` - Project data with tech stacks and highlights
- `ReadingListItem` - Reading list with categories
- `TechnicalImplementation` - Technical implementation tracking

**Important**: The live app uses JSON files, not the database. The ORM models exist for potential future migration or parallel features.

### Flask + Chromedriver Lifecycle Manager
`flask_driver_runner.py` is a **development utility** that:
- Runs Flask in a background thread
- Launches Chrome/Chromedriver automatically
- Monitors browser state and shuts down Flask when browser closes
- Useful for development/testing workflows that require browser automation

## Deployment Strategy

### Two-Branch Workflow
- **main**: Development branch (source of truth for code)
- **deploy**: Production branch (triggers CI/CD)

### Deployment Process for Code Changes
1. Work on `main` branch
2. Test locally with `pytest`
3. Run `./deploy.sh` which:
   - Runs complete pytest test suite
   - Runs code quality checks (flake8)
   - Validates JSON data files
   - Shows diff between main and deploy
   - Prompts for confirmation
   - Merges main → deploy
   - Pushes to trigger GitHub Actions
4. GitHub Actions (`.github/workflows/deploy.yml`) deploys to DigitalOcean (192.34.61.197)

### JSON Data Management
**IMPORTANT**: JSON data files in `data/` are NOT tracked in git (`.gitignore`).

#### Authentication Setup
All POST endpoints require bearer token authentication:

1. Generate a secure token:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. Create `.env` file (or copy from `.env.example`):
```bash
API_TOKEN=your-generated-token-here
```

3. Add the same token to production server's environment variables

#### Local Development Workflow
Test data changes locally first, then push to production:

**WARP Workflow for Adding Reading List Items:**
1. WARP asks user for book details (title, description, URL, category)
2. WARP generates the curl command with the book data
3. WARP starts Flask driver (`python flask_driver_runner.py app:app`)
4. User opens another terminal and runs the curl command
5. User verifies the data was added via browser or GET request
6. User runs the same curl command against production (`https://savantlab.org`)

**IMPORTANT**: WARP cannot send curl requests while Flask driver is running. User must run curl commands in a separate terminal window.

**Example curl commands:**
```bash
# 1. Test locally (Flask running on localhost:5001)
curl -X POST http://localhost:5001/api/reading-list/add \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "Book Title",
    "description": "Book description",
    "url": "https://example.com",
    "category": "Category",
    "completed": false
  }'

# 2. Verify locally in browser or via GET request
curl http://localhost:5001/api/reading-list

# 3. Push to production (same request, different URL)
curl -X POST https://savantlab.org/api/reading-list/add \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "title": "Book Title",
    "description": "Book description",
    "url": "https://example.com",
    "category": "Category",
    "completed": false
  }'
```

This separation ensures:
- Code changes go through git review and CI/CD
- Content updates are tested locally before production
- Production content updates happen instantly without deployment
- No merge conflicts between code and data changes
- Authenticated access prevents unauthorized modifications

### Critical Deployment Rules
**NEVER** make ANY changes (code, documentation, configuration, etc.) without explicit user permission. Always:
1. Propose the change
2. Ask: "Would you like me to make this change?"
3. Wait for confirmation
4. Then make the change

**NEVER** deploy automatically without user approval. Always:
1. Make changes
2. Show what changed
3. Ask: "Would you like me to commit and deploy these changes?"
4. Wait for confirmation
5. Then commit and push

The deploy workflow:
```bash
git checkout deploy
git merge main -m "Deploy: Merge main into deploy

Co-Authored-By: Warp <agent@warp.dev>"
git push origin deploy
```

## Code Patterns

### Adding New Routes
Routes follow a dual pattern: web routes + API endpoints
```python
# Web route (renders template)
@app.route("/page")
def page():
    return render_template("page.html", data=DATA)

# API endpoint (returns JSON)
@app.route("/api/page")
def api_page():
    return jsonify(DATA)
```

### Adding Data
To add new content:
1. Edit appropriate JSON file in `data/`
2. Validate JSON syntax: `python3 -m json.tool data/file.json`
3. Restart Flask to reload data

### Contact Microservice Pattern
To add a new contact microservice:
```python
# Load data
CONTACT_NEW = load_json_data('contact_new.json')

# Add to linked list
contact_services.append('new', '/api/contact/new', CONTACT_NEW)

# Add API endpoint
@app.route("/api/contact/new")
def api_contact_new():
    return jsonify(CONTACT_NEW)

# Add web route
@app.route("/contact/new")
def contact_new():
    node = contact_services.get('new')
    return render_template(f"contact_new.html", service=node)
```

## File Structure Context

### Application Core
- `app.py` - Flask application with routes and business logic
- `contact_list.py` - Linked list data structure for contact microservices
- `flask_driver_runner.py` - Development utility for Flask + browser lifecycle

### Data Layer (Active)
- `data/*.json` - All application content (projects, publications, contact info)
- **Note**: `data/` directory is in `.gitignore` and NOT tracked in version control

### Database Layer (Inactive)
- `database.py` - SQLAlchemy initialization
- `models.py` - ORM models (BlogPost, Project, ReadingListItem, TechnicalImplementation)
- `blog.py`, `projects.py`, `technical_implementation.py` - Database service modules

### Templates
- `templates/index.html` - Homepage with projects/publications
- `templates/about.html` - About page
- `templates/contact.html` - Contact landing page
- `templates/contact_*.html` - Individual contact microservice pages
- `templates/project.html` - Individual project detail page
- `templates/journal.html` - Academic journal page
- `templates/counterterrorism.html` - Counterterrorism research page

### DevOps
- `deploy.sh` - Automated deployment validation and execution
- `.github/workflows/deploy.yml` - GitHub Actions CI/CD pipeline
- `requirements.txt` - Python dependencies

## Dependencies
- **Flask** (3.0.0) - Web framework
- **Gunicorn** (21.2.0) - Production WSGI server
- **Selenium** (≥4.0.0) - Browser automation
- **webdriver-manager** (≥3.8.0) - Chromedriver management
- **markdown** (≥3.5.0) - Markdown processing

## Important Constraints

### Testing Framework
The project uses **pytest** for comprehensive testing:
- `tests/test_app.py` - Complete test suite covering:
  - Data structure validation
  - Web route testing (all pages)
  - API endpoint testing (all endpoints)
  - Linked list implementation testing
  - Error handling and 404 responses
- `pytest.ini` - Pytest configuration with coverage settings
- Tests are integrated into `deploy.sh` and run automatically before deployment
- Coverage reports generated in HTML format (`htmlcov/`)

### JSON Data Source
All content comes from JSON files. Changes require:
1. Edit JSON file
2. Validate JSON syntax
3. Restart Flask app

### No Environment Variables Required
The app runs without environment variables for basic functionality. Optional:
- `DATABASE_URL` - If using PostgreSQL instead of SQLite (currently unused)

## Version Control Best Practices

### Commit Messages
Include co-author attribution:
```
Commit message

Co-Authored-By: Warp <agent@warp.dev>
```

### Branch Hygiene
- Keep `main` as source of truth for development
- Only merge to `deploy` when ready for production
- `deploy` branch triggers automatic deployment to production

## Common Workflows

### Adding a New Project
1. Edit `data/projects.json`
2. Add project object with required keys: `id`, `title`, `subtitle`, `description`, `tech`, `highlights`, `github`, `status`, `image`
3. Validate: `python3 -m json.tool data/projects.json`
4. Test: `python app.py` and visit `http://localhost:5001`

### Running Tests for Specific Features
```bash
# Test data structures
pytest tests/test_app.py::TestDataStructures -v

# Test web routes
pytest tests/test_app.py::TestWebRoutes -v

# Test API endpoints
pytest tests/test_app.py::TestAPIEndpoints -v

# Test linked list implementation
pytest tests/test_app.py::TestLinkedListImplementation -v
```

### Debugging Data Issues
```python
# Quick data check
python3 -c "
from app import PROJECTS, PUBLICATIONS, ABOUT, CONTACT
print('Projects:', len(PROJECTS))
print('Publications:', len(PUBLICATIONS))
print('About sections:', ABOUT.keys())
print('Contact info:', CONTACT.keys())
"
```

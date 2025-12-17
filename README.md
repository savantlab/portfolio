# Savantlab Portfolio

Full-stack portfolio website for Stephanie King - Cognitive Scientist and Full-Stack Software Engineer. Showcases research breakthroughs, software projects, and technical infrastructure.

## Features

**Research & Content**
- **Research Breakthrough** - Mental Rotation Paradox resolution
- **Projects** - 5 active research and software projects
- **Blog** - Technical writing with tagging and archival
- **Reading List** - Curated research materials with tracking
- **Publications** - Papers in development
- **Academic Journal** - Cognitive Constraint (coming soon)

**Technical Stack**
- **Full-Stack Application** - Flask backend with responsive HTML/CSS/JS frontend
- **Persistent Database** - PostgreSQL with SQLAlchemy ORM
- **Container Orchestration** - Docker Compose with multi-service setup
- **REST APIs** - Complete CRUD endpoints for all data models
- **CLI Tools** - Command-line interface for reading list management

## Local Development

### Quick Start with Docker Compose

The recommended way to run the full application with PostgreSQL database:

```bash
# Copy environment template
cp .env.example .env

# Start services (Flask + PostgreSQL)
docker-compose up --build
```

The app will be available at `http://localhost:5001` and PostgreSQL at `localhost:5432`.

### Local Development (without Docker)

**Install Dependencies:**

```bash
pip install -r requirements.txt
```

**Configure Environment:**

```bash
cp .env.example .env
# Edit .env for local SQLite or PostgreSQL connection
```

### Setup Chromedriver (Optional)

To enable Selenium-based automation and testing:

```bash
python setup_chromedriver.py
```

This automatically downloads chromedriver matching your Chrome browser version and creates a `chromedriver_config.py` module.

**Usage in code:**
```python
from chromedriver_config import get_chrome_driver

driver = get_chrome_driver()  # Regular mode
driver = get_chrome_driver(headless=True)  # Headless mode
```

**Run Development Server:**

```bash
python app.py
```

Visit `http://localhost:5001`. By default uses SQLite database (`savantlab.db`).

### Run with Chromedriver Lifecycle Management

To run the Flask app with chromedriver, where the app automatically shuts down when you close the browser:

```bash
python flask_driver_runner.py app:app
```

**Options:**
- `--headless`: Run Chrome in headless mode (no visible window)
- `--port PORT`: Specify port (default: 5001)
- `--host HOST`: Specify host (default: 127.0.0.1)

**Examples:**
```bash
# Run with visible Chrome window
python flask_driver_runner.py app:app

# Run in headless mode
python flask_driver_runner.py app:app --headless

# Custom port
python flask_driver_runner.py app:app --port 5002
```

**Programmatic Usage:**
```python
from flask_driver_runner import run_app_with_driver

driver = run_app_with_driver(app, headless=True)
driver.get("http://localhost:5001")
# App automatically shuts down when driver closes
```

## Database

### PostgreSQL (Docker Compose)

When running with `docker-compose up`, PostgreSQL is automatically started:

```bash
# Access PostgreSQL directly
psql -h localhost -U postgres -d savantlab
```

Data is persisted in `postgres_data` volume.

### SQLite (Local Development)

By default, local development uses SQLite. Database file: `savantlab.db`

### Environment Variables

```bash
# PostgreSQL connection (overrides SQLite)
DATABASE_URL=postgresql://user:password@localhost:5432/savantlab

# Or individual settings
DB_NAME=savantlab
DB_USER=postgres
DB_PASSWORD=postgres
```

## API Endpoints

**Blog**
- `GET /api/blog` - List published posts
- `POST /api/blog` - Create post
- `GET /api/blog/<id>` - Get specific post
- `GET /api/blog/tags` - List all tags
- `GET /api/blog/tags/<tag>` - Posts by tag

**Projects**
- `GET /api/projects` - List all projects
- `POST /api/projects` - Add project
- `GET /api/projects/<id>` - Get specific project
- `PUT /api/projects/<id>` - Update project
- `DELETE /api/projects/<id>` - Delete project

**Reading List** (requires auth token)
- `POST /api/auth/token` - Request token
- `POST /api/auth/verify` - Verify token
- `GET /api/reading-list` - List items
- `POST /api/reading-list` - Add item
- `PUT/DELETE /api/reading-list/<id>` - Update/delete item

**Technical Implementations**
- `GET /api/technical-implementations` - List implementations
- `POST /api/technical-implementations` - Add implementation
- `GET/PUT/DELETE /api/technical-implementations/<id>` - Manage items

## Production Deployment

### Using Docker Compose (Recommended)

```bash
docker-compose up -d
```

App runs with Gunicorn (4 workers) on port 5001.

### Manual Deployment

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Requires `DATABASE_URL` environment variable pointing to PostgreSQL.

## Project Structure

```
savantlab-portfolio/
├── app.py                           # Flask application with routes
├── database.py                      # SQLAlchemy initialization
├── models.py                        # ORM models (BlogPost, Project, etc.)
├── blog.py                          # Blog storage module
├── projects.py                      # Projects storage module
├── reading_list.py                  # Reading list storage module
├── technical_implementation.py      # Technical implementations storage
├── auth.py                          # Authentication module
├── reading_list_cli.py              # CLI tool for reading list
├── flask_driver_runner.py           # Flask + Chromedriver lifecycle manager
├── requirements.txt                 # Python dependencies
├── docker-compose.yml               # Multi-container orchestration
├── Dockerfile                       # Flask app container
├── .env.example                     # Environment variables template
├── templates/                       # HTML templates
│   ├── index.html                 # Homepage
│   ├── blog.html                  # Blog listing
│   ├── blog_post.html             # Individual post
│   ├── about.html                 # About page
│   ├── contact.html               # Contact page
│   ├── journal.html               # Journal page
│   ├── reading_list.html          # Reading list page
│   ├── counterterrorism.html      # Project page
│   └── project.html               # Dynamic project template
├── static/                          # Static assets
│   ├── css/style.css              # Main stylesheet
│   ├── js/script.js               # JavaScript
│   └── images/                    # Project images
└── README.md                        # This file
```

## Architecture

**Two-Branch Strategy:**
- `main` - Production-ready minimal deployment (Flask + templates only)
- `deploy` - Full development environment (all tools, scripts, infrastructure)

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed deployment strategy.

**Database:**
- SQLAlchemy ORM with PostgreSQL (production) or SQLite (development)
- 4 main models: BlogPost, Project, ReadingListItem, TechnicalImplementation
- Persistent volume storage in Docker Compose

**API Design:**
- RESTful endpoints for all data models
- Token-based authentication for sensitive operations
- JSON request/response format
- CORS-friendly responses

## License

© 2025 Savantlab. All rights reserved.

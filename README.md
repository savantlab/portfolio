# Savantlab Portfolio

Professional portfolio website for Stephanie King - Cognitive Scientist, showcasing research breakthroughs, projects, and the Cognitive Constraint academic journal.

## Features

- **Hero Section** - Introduction and credentials
- **Research Breakthrough** - Mental Rotation Paradox resolution
- **Academic Journal** - Cognitive Constraint (coming soon)
- **Projects** - Detailed project showcases with GitHub links
- **Publications** - Papers in development
- **Contact** - Research collaboration information
- **Responsive Design** - Mobile-friendly layout

## Local Development

### Install Dependencies

```bash
pip install -r requirements.txt
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

### Run Development Server

```bash
python app.py
```

Visit `http://localhost:5001`

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

## Production Deployment

### Using Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables

None required for basic functionality.

## Project Structure

```
savantlab-portfolio/
├── app.py                      # Flask application
├── requirements.txt            # Python dependencies
├── flask_driver_runner.py      # Flask + Chromedriver lifecycle manager
├── setup_chromedriver.py       # Setup script for chromedriver
├── chromedriver_config.py      # Auto-generated chromedriver config (after setup)
├── example_driver_usage.py     # Usage examples
├── .env.development            # Development environment config
├── templates/                  # HTML templates
│   ├── index.html             # Homepage
│   ├── about.html             # About page
│   ├── contact.html           # Contact page
│   └── journal.html           # Journal page
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   └── js/
│       └── script.js          # JavaScript interactions
└── README.md                   # This file
```

## License

© 2025 Savantlab. All rights reserved.

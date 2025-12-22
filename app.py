from flask import Flask, render_template
import os

app = Flask(__name__)

# Project data
PROJECTS = [
    {
        "id": "mental-rotation",
        "title": "Mental Rotation Research Platform",
        "subtitle": "Resolving the Mental Rotation Paradox in Cognitive Science",
        "description": "Comprehensive ML pipeline for systematic literature analysis invalidating the allocentric model of spatial cognition—a theoretical framework that failed to constrain mental rotation despite decades of acceptance.",
        "tech": ["Python", "scikit-learn", "d6tflow", "NLP", "TF-IDF", "LDA", "Random Forest"],
        "highlights": [
            "280+ papers analyzed (1970-present)",
            "6-stage ML workflow for topic discovery and citation prediction",
            "Publication-ready Python library with CLI tools",
            "Automated research infrastructure with async web scraping"
        ],
        "github": "https://github.com/savantlab/mental-rotation-research",
        "status": "Active Research",
        "image": None
    },
    {
        "id": "parallel-critiques",
        "title": "Parallel Critiques: Analyzing Rhetorical Extremism",
        "subtitle": "Computational Discourse Analysis of Ideological Transmission",
        "description": "Rigorous NLP analysis comparing Jordan Peterson's academic discourse with Nazi Anders Breivik's extremist manifesto, revealing textual and conceptual overlap, transformation points from abstract critique to concrete threat identification, and rhetorical patterns that mask dangerous ideologies.",
        "tech": ["Python", "scikit-learn", "NetworkX", "TF-IDF", "N-gram Analysis", "Network Co-occurrence"],
        "highlights": [
            "16% semantic similarity, 75% conceptual overlap identified",
            "Network density analysis: 3x difference between abstract vs operationalized ideologies",
            "Mapped implicit terminology frameworks showing vocabulary masking",
            "Interactive Jupyter notebooks with visualization dashboards"
        ],
        "github": None,
        "status": "Manuscript in Preparation",
        "image": "parallel-2.png"
    },
    {
        "id": "mouse-trackpad",
        "title": "Mouse-Trackpad Science Lab",
        "subtitle": "Computational Analysis of Human-Computer Interaction Patterns",
        "description": "Experimental platform for analyzing motor control and decision-making patterns through cursor tracking and interaction metrics.",
        "tech": ["Python", "pandas", "matplotlib", "Data Analysis", "Eye Tracking"],
        "highlights": [
            "Real-time session analysis and processing",
            "Comprehensive metrics and visualization tools",
            "Left-right analysis for motor control patterns"
        ],
        "github": None,
        "status": "Experimental",
        "image": None
    },
    {
        "id": "osiris-deception",
        "title": "The Depth of Deception: Jordan Peterson's Fraud Story",
        "subtitle": "Exposing Misrepresentation of Ancient Egyptian Symbolism",
        "description": "Analysis revealing how Jordan Peterson fundamentally misrepresented the meaning of Osiris in ancient Egyptian theology, falsely claiming it signified the living and dead pharaoh when it never held that meaning to the ancient Egyptians.",
        "tech": ["Historical Analysis", "Egyptology", "Symbolic Systems", "Critical Examination"],
        "highlights": [
            "Documented misuse of ancient Egyptian symbolism",
            "Examination of Osiris's actual theological significance",
            "Analysis of how incorrect meanings were propagated",
            "Scholarly sources contradicting Peterson's claims"
        ],
        "github": None,
        "status": "Research in Progress",
        "image": None
    },
    {
        "id": "tax-budget",
        "title": "Tax Budget Allocator",
        "subtitle": "Enterprise-Scale Budget Planning with Multi-Container Orchestration",
        "description": "Production-ready Django application with multi-container Docker Compose architecture. Uses Redis for caching and as a Celery broker, SQLite for persistence, Gunicorn for WSGI, optional Nginx reverse proxy, and Celery workers/beat for background and scheduled jobs. Demonstrates solving operational complexity via health checks, service dependencies, and persistent volumes.",
        "tech": ["Django", "Docker Compose", "SQLite", "Redis", "Celery", "Flower", "Nginx", "Gunicorn", "Python", "JavaScript"],
        "highlights": [
            "Multi-container orchestration (db, redis, web, celery, celery-beat, flower, nginx)",
            "Redis-backed caching and message brokering with AOF persistence",
            "Automated health checks and dependency gating for startup",
            "Background processing via Celery workers and periodic tasks via Celery Beat",
            "Operational observability through Flower dashboard",
            "SQLite with volume-backed data persistence and migrations",
            "Interactive budget allocation and aggregate reporting interfaces"
        ],
        "github": "https://github.com/savantlab/taxbudget",
        "status": "Active Development",
        "image": None
    },
    {
        "id": "mad-scientist",
        "title": "Mad Scientist AI",
        "subtitle": "Production AI Chat Interface with Cloudflare Workers AI",
        "description": "Full-stack AI chat application built with FastAPI and Cloudflare Workers AI. Features production-ready deployment configurations for multiple platforms (Coolify, Railway, Render, AWS ECS, Docker, VPS), comprehensive health monitoring, and enterprise-grade infrastructure with reverse proxy support and SSL automation. Solves the common chatbot UI problem of routing AI-generated images from API responses to the dashboard.",
        "tech": ["Python", "FastAPI", "Uvicorn", "Cloudflare AI", "Docker", "Docker Compose", "AWS ECS", "Nginx", "Traefik"],
        "highlights": [
            "Solved image routing for AI-generated content (avatars, generated images) in chat interfaces",
            "Multi-platform deployment (Coolify, Railway, Render, AWS ECS, bare metal)",
            "Production Docker architecture with health checks and service dependencies",
            "Cloudflare Workers AI integration for scalable inference",
            "Automated SSL/TLS certificate management",
            "Reverse proxy configuration (Traefik/Nginx) for high availability",
            "Systemd service integration for bare metal deployments",
            "Comprehensive deployment scripts and documentation"
        ],
        "github": "https://github.com/stepheweffie/mad-scientist",
        "status": "Production Ready",
        "image": None
    }
]

PUBLICATIONS = [
    {
        "title": "The Surreal Art of Mental Rotation",
        "status": "Manuscript in Preparation",
        "description": "Challenges the prevailing allocentric model of spatial cognition using computational analysis of 50+ years of mental rotation research."
    },
    {
        "title": "Parallel Critiques: Analyzing Rhetorical Extremism",
        "status": "Technical Monograph in Development",
        "description": "Network co-occurrence analysis revealing how shared vocabulary masks fundamentally different conceptual architectures."
    }
]

@app.route("/")
def index():
    return render_template("index.html", projects=PROJECTS, publications=PUBLICATIONS)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/project/<project_id>")
def project_detail(project_id):
    project = next((p for p in PROJECTS if p["id"] == project_id), None)
    if not project:
        return "Project not found", 404
    return render_template("project.html", project=project)

@app.route("/journal")
def journal():
    return render_template("journal.html")

@app.route("/counterterrorism")
def counterterrorism():
    return render_template("counterterrorism.html")


@app.route("/healthz")
def healthz():
    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

"""
Projects Storage Module
Manages projects data with API support
"""
from database import db
from models import Project

# Default projects data for seeding
DEFAULT_PROJECTS = [
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
        "id": "digital-product",
        "title": "Digital Product Platform",
        "subtitle": "E-Commerce System with Content Management and Automated Communications",
        "description": "Full-featured e-commerce platform combining shopping cart functionality, integrated blog system, and automated email server for customer communications. Handles product inventory management, secure checkout processes, content publishing, and transactional email delivery. Demonstrates integration of multiple systems (commerce, content, messaging) into a cohesive platform.",
        "tech": ["Python", "Flask/Django", "PostgreSQL", "Stripe/Payment Integration", "Email Servers", "Blog CMS", "Cart Management"],
        "highlights": [
            "Complete shopping cart with product inventory and checkout flow",
            "Integrated blog system for product content and marketing",
            "Automated email server handling transactional and promotional communications",
            "Secure payment processing and order management",
            "Customer account management and purchase history",
            "Email template system for customizable customer communications"
        ],
        "github": "https://github.com/savantlab/digital_product",
        "status": "Active Development",
        "image": None
    }
]

def get_all_projects() -> list:
    """Get all projects"""
    projects = Project.query.all()
    return [p.to_dict() for p in projects]


def get_project(project_id: str) -> dict:
    """Get a specific project by ID"""
    project = Project.query.get(project_id)
    return project.to_dict() if project else None


def add_project(title: str, subtitle: str, description: str, tech: list,
                highlights: list, github: str = None, status: str = "Active",
                image: str = None) -> dict:
    """Add a new project"""
    if not title or not subtitle or not description:
        raise ValueError("Title, subtitle, and description are required")
    
    # Generate ID from title
    project_id = title.lower().replace(" ", "-")[:50]
    
    if Project.query.get(project_id):
        raise ValueError(f"Project ID {project_id} already exists")
    
    project = Project(
        id=project_id,
        title=title,
        subtitle=subtitle,
        description=description,
        tech=tech,
        highlights=highlights,
        github=github,
        status=status,
        image=image
    )
    
    db.session.add(project)
    db.session.commit()
    return project.to_dict()


def update_project(project_id: str, **kwargs) -> dict:
    """Update a project"""
    project = Project.query.get(project_id)
    if not project:
        return None
    
    allowed_fields = {"title", "subtitle", "description", "tech", "highlights", "github", "status", "image"}
    for field in allowed_fields:
        if field in kwargs:
            setattr(project, field, kwargs[field])
    
    db.session.commit()
    return project.to_dict()


def delete_project(project_id: str) -> bool:
    """Delete a project"""
    project = Project.query.get(project_id)
    if not project:
        return False
    
    db.session.delete(project)
    db.session.commit()
    return True


def seed_default_projects() -> None:
    """Seed database with default projects if empty"""
    if Project.query.first():
        return
    
    for proj in DEFAULT_PROJECTS:
        project = Project(**proj)
        db.session.add(project)
    
    db.session.commit()

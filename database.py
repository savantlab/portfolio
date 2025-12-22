"""
Database initialization and configuration for Flask-SQLAlchemy
"""
import os
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()


def init_db(app):
    """Initialize database with Flask app"""
    # Configure database URL from environment or use SQLite as fallback
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # PostgreSQL
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # SQLite fallback for development
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///savantlab.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return db

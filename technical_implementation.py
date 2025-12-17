"""
Technical Implementation Storage Module - Database-backed
Manages technical implementation items with SQLAlchemy
"""
from database import db
from models import TechnicalImplementation


def add_implementation(title: str, description: str, tech_stack: list = None, status: str = "Active") -> dict:
    """Add a new technical implementation"""
    if not title or not description:
        raise ValueError("Title and description are required")
    
    impl = TechnicalImplementation(
        title=title,
        description=description,
        tech_stack=tech_stack or [],
        status=status
    )
    
    db.session.add(impl)
    db.session.commit()
    
    return impl.to_dict()


def get_all_implementations() -> list:
    """Get all technical implementations"""
    impls = TechnicalImplementation.query.order_by(TechnicalImplementation.created_at.desc()).all()
    return [i.to_dict() for i in impls]


def get_implementation(item_id: int) -> dict:
    """Get a specific implementation"""
    impl = TechnicalImplementation.query.get(item_id)
    return impl.to_dict() if impl else None


def update_implementation(item_id: int, **kwargs) -> dict:
    """Update an implementation"""
    impl = TechnicalImplementation.query.get(item_id)
    if not impl:
        return None
    
    if "title" in kwargs:
        impl.title = kwargs["title"]
    if "description" in kwargs:
        impl.description = kwargs["description"]
    if "tech_stack" in kwargs:
        impl.tech_stack = kwargs["tech_stack"]
    if "status" in kwargs:
        impl.status = kwargs["status"]
    
    db.session.commit()
    return impl.to_dict()


def delete_implementation(item_id: int) -> bool:
    """Delete an implementation"""
    impl = TechnicalImplementation.query.get(item_id)
    if not impl:
        return False
    
    db.session.delete(impl)
    db.session.commit()
    return True

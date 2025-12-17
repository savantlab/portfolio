"""
Reading List Storage Module - Database-backed
Manages reading list items with SQLAlchemy
"""
from database import db
from models import ReadingListItem


def add_item(title: str, url: str = None, description: str = None, category: str = None) -> dict:
    """Add a new reading list item"""
    if not title:
        raise ValueError("Title is required")
    
    item = ReadingListItem(
        title=title,
        url=url,
        description=description,
        category=category
    )
    
    db.session.add(item)
    db.session.commit()
    
    return item.to_dict()


def get_all_items() -> list:
    """Get all reading list items"""
    items = ReadingListItem.query.order_by(ReadingListItem.created_at.desc()).all()
    return [i.to_dict() for i in items]


def get_item(item_id: int) -> dict:
    """Get a specific reading list item"""
    item = ReadingListItem.query.get(item_id)
    return item.to_dict() if item else None


def update_item(item_id: int, **kwargs) -> dict:
    """Update a reading list item"""
    item = ReadingListItem.query.get(item_id)
    if not item:
        return None
    
    if "title" in kwargs:
        item.title = kwargs["title"]
    if "url" in kwargs:
        item.url = kwargs["url"]
    if "description" in kwargs:
        item.description = kwargs["description"]
    if "category" in kwargs:
        item.category = kwargs["category"]
    if "completed" in kwargs:
        item.completed = kwargs["completed"]
    
    db.session.commit()
    return item.to_dict()


def toggle_completed(item_id: int) -> dict:
    """Toggle completed status of an item"""
    item = ReadingListItem.query.get(item_id)
    if not item:
        return None
    
    item.completed = not item.completed
    db.session.commit()
    return item.to_dict()


def delete_item(item_id: int) -> bool:
    """Delete a reading list item"""
    item = ReadingListItem.query.get(item_id)
    if not item:
        return False
    
    db.session.delete(item)
    db.session.commit()
    return True

"""
Technical Implementation Row Items Storage
Stores and manages technical implementation notes that can be displayed on pages
"""
from datetime import datetime
from typing import List, Dict, Optional

# In-memory storage (will be lost on server restart)
_implementations: Dict[int, Dict] = {}
_next_id = 1


def add_implementation(title: str, description: str, tech_stack: List[str] = None, 
                      status: str = "Active") -> Dict:
    """Add a new technical implementation row item"""
    global _next_id
    
    if not title or not description:
        raise ValueError("Title and description are required")
    
    item = {
        "id": _next_id,
        "title": title,
        "description": description,
        "tech_stack": tech_stack or [],
        "status": status,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    _implementations[_next_id] = item
    _next_id += 1
    
    return item


def get_all_implementations() -> List[Dict]:
    """Get all technical implementations"""
    return sorted(_implementations.values(), key=lambda x: x["id"], reverse=True)


def get_implementation(item_id: int) -> Optional[Dict]:
    """Get a specific implementation by ID"""
    return _implementations.get(item_id)


def update_implementation(item_id: int, **kwargs) -> Optional[Dict]:
    """Update an implementation"""
    if item_id not in _implementations:
        return None
    
    item = _implementations[item_id]
    
    # Allow updating title, description, tech_stack, status
    if "title" in kwargs:
        item["title"] = kwargs["title"]
    if "description" in kwargs:
        item["description"] = kwargs["description"]
    if "tech_stack" in kwargs:
        item["tech_stack"] = kwargs["tech_stack"]
    if "status" in kwargs:
        item["status"] = kwargs["status"]
    
    item["updated_at"] = datetime.now().isoformat()
    return item


def delete_implementation(item_id: int) -> bool:
    """Delete an implementation"""
    if item_id in _implementations:
        del _implementations[item_id]
        return True
    return False


def clear_all() -> None:
    """Clear all implementations (for testing)"""
    global _implementations, _next_id
    _implementations = {}
    _next_id = 1

"""
Blog Storage Module
Manages blog posts with API support
"""
from datetime import datetime
from typing import List, Dict, Optional

# In-memory storage
_posts: Dict[int, Dict] = {}
_next_id = 1


def add_post(title: str, content: str, tags: List[str] = None, 
             published: bool = True) -> Dict:
    """Add a new blog post"""
    global _next_id
    
    if not title or not content:
        raise ValueError("Title and content are required")
    
    post = {
        "id": _next_id,
        "title": title,
        "content": content,
        "tags": tags or [],
        "published": published,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    _posts[_next_id] = post
    _next_id += 1
    
    return post


def get_all_posts(published_only: bool = True) -> List[Dict]:
    """Get all blog posts, optionally filtered to published only"""
    posts = _posts.values()
    if published_only:
        posts = [p for p in posts if p.get("published")]
    return sorted(posts, key=lambda x: x["created_at"], reverse=True)


def get_post(post_id: int) -> Optional[Dict]:
    """Get a specific post by ID"""
    return _posts.get(post_id)


def update_post(post_id: int, **kwargs) -> Optional[Dict]:
    """Update a blog post"""
    if post_id not in _posts:
        return None
    
    post = _posts[post_id]
    
    # Allow updating title, content, tags, published
    if "title" in kwargs:
        post["title"] = kwargs["title"]
    if "content" in kwargs:
        post["content"] = kwargs["content"]
    if "tags" in kwargs:
        post["tags"] = kwargs["tags"]
    if "published" in kwargs:
        post["published"] = kwargs["published"]
    
    post["updated_at"] = datetime.now().isoformat()
    return post


def delete_post(post_id: int) -> bool:
    """Delete a blog post"""
    if post_id in _posts:
        del _posts[post_id]
        return True
    return False


def get_posts_by_tag(tag: str, published_only: bool = True) -> List[Dict]:
    """Get posts by tag"""
    posts = [p for p in _posts.values() if tag in p.get("tags", [])]
    if published_only:
        posts = [p for p in posts if p.get("published")]
    return sorted(posts, key=lambda x: x["created_at"], reverse=True)


def get_all_tags(published_only: bool = True) -> List[str]:
    """Get all unique tags"""
    tags = set()
    for post in _posts.values():
        if published_only and not post.get("published"):
            continue
        tags.update(post.get("tags", []))
    return sorted(list(tags))


def clear_all() -> None:
    """Clear all posts (for testing)"""
    global _posts, _next_id
    _posts = {}
    _next_id = 1

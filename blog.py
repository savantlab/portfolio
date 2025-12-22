"""
Blog Storage Module - Database-backed
Manages blog posts with SQLAlchemy
"""
from database import db
from models import BlogPost


def add_post(title: str, content: str, tags: list = None, published: bool = True) -> dict:
    """Add a new blog post"""
    if not title or not content:
        raise ValueError("Title and content are required")
    
    post = BlogPost(
        title=title,
        content=content,
        tags=tags or [],
        published=published
    )
    
    db.session.add(post)
    db.session.commit()
    
    return post.to_dict()


def get_all_posts(published_only: bool = True) -> list:
    """Get all blog posts"""
    query = BlogPost.query
    if published_only:
        query = query.filter_by(published=True)
    
    posts = query.order_by(BlogPost.created_at.desc()).all()
    return [p.to_dict() for p in posts]


def get_post(post_id: int) -> dict:
    """Get a specific post by ID"""
    post = BlogPost.query.get(post_id)
    return post.to_dict() if post else None


def update_post(post_id: int, **kwargs) -> dict:
    """Update a blog post"""
    post = BlogPost.query.get(post_id)
    if not post:
        return None
    
    if "title" in kwargs:
        post.title = kwargs["title"]
    if "content" in kwargs:
        post.content = kwargs["content"]
    if "tags" in kwargs:
        post.tags = kwargs["tags"]
    if "published" in kwargs:
        post.published = kwargs["published"]
    
    db.session.commit()
    return post.to_dict()


def delete_post(post_id: int) -> bool:
    """Delete a blog post"""
    post = BlogPost.query.get(post_id)
    if not post:
        return False
    
    db.session.delete(post)
    db.session.commit()
    return True


def get_posts_by_tag(tag: str, published_only: bool = True) -> list:
    """Get posts by tag"""
    query = BlogPost.query.filter(BlogPost.tags.contains([tag]))
    if published_only:
        query = query.filter_by(published=True)
    
    posts = query.order_by(BlogPost.created_at.desc()).all()
    return [p.to_dict() for p in posts]


def get_all_tags(published_only: bool = True) -> list:
    """Get all unique tags"""
    query = BlogPost.query
    if published_only:
        query = query.filter_by(published=True)
    
    posts = query.all()
    tags = set()
    for post in posts:
        tags.update(post.tags or [])
    
    return sorted(list(tags))

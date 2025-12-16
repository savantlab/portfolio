"""
Reading list storage and management.
Items are stored in memory during runtime.
"""

# In-memory storage for reading list items
reading_list = []
item_counter = 0


def add_item(title, url=None, description=None, category=None):
    """Add an item to the reading list."""
    global item_counter
    item_counter += 1
    
    item = {
        "id": item_counter,
        "title": title,
        "url": url,
        "description": description,
        "category": category or "General",
        "completed": False
    }
    reading_list.append(item)
    return item


def get_all_items():
    """Get all reading list items."""
    return reading_list


def get_item(item_id):
    """Get a specific reading list item by ID."""
    for item in reading_list:
        if item["id"] == item_id:
            return item
    return None


def update_item(item_id, **kwargs):
    """Update a reading list item."""
    item = get_item(item_id)
    if item:
        for key, value in kwargs.items():
            if key in item:
                item[key] = value
        return item
    return None


def delete_item(item_id):
    """Delete a reading list item."""
    global reading_list
    reading_list = [item for item in reading_list if item["id"] != item_id]
    return True


def toggle_completed(item_id):
    """Toggle the completed status of an item."""
    item = get_item(item_id)
    if item:
        item["completed"] = not item["completed"]
        return item
    return None

"""
Linked List implementation for Contact Microservices
Each node represents a contact microservice with its own endpoint and data
"""

class ContactNode:
    """Node in the contact microservices linked list"""
    def __init__(self, service_id, endpoint, data):
        self.service_id = service_id
        self.endpoint = endpoint
        self.data = data
        self.next = None
    
    def __repr__(self):
        return f"ContactNode(id='{self.service_id}', endpoint='{self.endpoint}')"


class ContactLinkedList:
    """Linked list of contact microservices"""
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def append(self, service_id, endpoint, data):
        """Add a new contact microservice to the end of the list"""
        new_node = ContactNode(service_id, endpoint, data)
        
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        
        self.size += 1
        return new_node
    
    def get(self, service_id):
        """Get a microservice by ID"""
        current = self.head
        while current:
            if current.service_id == service_id:
                return current
            current = current.next
        return None
    
    def traverse(self):
        """Generator to traverse the linked list"""
        current = self.head
        while current:
            yield current
            current = current.next
    
    def to_list(self):
        """Convert linked list to Python list for JSON serialization"""
        return [
            {
                'id': node.service_id,
                'endpoint': node.endpoint,
                'data': node.data
            }
            for node in self.traverse()
        ]
    
    def __repr__(self):
        nodes = []
        current = self.head
        while current:
            nodes.append(current.service_id)
            current = current.next
        return f"ContactLinkedList({' -> '.join(nodes)})"
    
    def __len__(self):
        return self.size

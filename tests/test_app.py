"""
Test suite for Flask application
"""
import pytest
import json
from app import app, PROJECTS, PUBLICATIONS, ABOUT, CONTACT, contact_services


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestDataStructures:
    """Test data integrity and structure"""
    
    def test_projects_structure(self):
        """Validate all projects have required fields"""
        required_keys = ['id', 'title', 'subtitle', 'description', 'tech', 'highlights', 'github', 'status', 'image']
        
        assert len(PROJECTS) > 0, "No projects loaded"
        
        for project in PROJECTS:
            for key in required_keys:
                assert key in project, f"Project {project.get('id', 'unknown')} missing key: {key}"
            
            assert isinstance(project['tech'], list), f"Project {project['id']} tech must be a list"
            assert isinstance(project['highlights'], list), f"Project {project['id']} highlights must be a list"
            assert isinstance(project['id'], str), f"Project id must be a string"
    
    def test_publications_structure(self):
        """Validate all publications have required fields"""
        required_keys = ['title', 'status', 'description']
        
        assert len(PUBLICATIONS) > 0, "No publications loaded"
        
        for pub in PUBLICATIONS:
            for key in required_keys:
                assert key in pub, f"Publication {pub.get('title', 'unknown')} missing key: {key}"
    
    def test_about_structure(self):
        """Validate about data structure"""
        assert isinstance(ABOUT, dict), "ABOUT must be a dictionary"
        assert len(ABOUT) > 0, "ABOUT data is empty"
    
    def test_contact_structure(self):
        """Validate contact data structure"""
        assert isinstance(CONTACT, dict), "CONTACT must be a dictionary"
        assert len(CONTACT) > 0, "CONTACT data is empty"
    
    def test_contact_services_linked_list(self):
        """Validate contact services linked list structure"""
        assert contact_services.head is not None, "Contact services linked list is empty"
        assert len(contact_services) > 0, "Contact services linked list has no items"
        
        # Test linked list traversal
        nodes = list(contact_services.traverse())
        assert len(nodes) == len(contact_services), "Linked list traversal count mismatch"
        
        # Test that all nodes have required attributes
        for node in nodes:
            assert hasattr(node, 'service_id')
            assert hasattr(node, 'endpoint')
            assert hasattr(node, 'data')


class TestWebRoutes:
    """Test web page routes"""
    
    def test_homepage(self, client):
        """Test homepage loads successfully"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Stephanie King' in response.data or b'Savantlab' in response.data
    
    def test_about_page(self, client):
        """Test about page loads successfully"""
        response = client.get('/about')
        assert response.status_code == 200
    
    def test_contact_page(self, client):
        """Test contact page loads successfully"""
        response = client.get('/contact')
        assert response.status_code == 200
    
    def test_journal_page(self, client):
        """Test journal page loads successfully"""
        response = client.get('/journal')
        assert response.status_code == 200
    
    def test_counterterrorism_page(self, client):
        """Test counterterrorism page loads successfully"""
        response = client.get('/counterterrorism')
        assert response.status_code == 200
    
    def test_healthz_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/healthz')
        assert response.status_code == 200
        data = response.get_json()
        assert data['ok'] is True
    
    def test_project_detail_routes(self, client):
        """Test all project detail pages load"""
        for project in PROJECTS:
            response = client.get(f'/project/{project["id"]}')
            assert response.status_code == 200, f"Project {project['id']} failed to load"
    
    def test_contact_microservice_routes(self, client):
        """Test contact microservice pages"""
        for node in contact_services.traverse():
            response = client.get(f'/contact/{node.service_id}')
            assert response.status_code == 200, f"Contact service {node.service_id} failed to load"
    
    def test_nonexistent_project(self, client):
        """Test 404 for nonexistent project"""
        response = client.get('/project/nonexistent-project-xyz')
        assert response.status_code == 404
    
    def test_nonexistent_contact_service(self, client):
        """Test 404 for nonexistent contact service"""
        response = client.get('/contact/nonexistent-service-xyz')
        assert response.status_code == 404


class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_api_projects(self, client):
        """Test projects API endpoint"""
        response = client.get('/api/projects')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == len(PROJECTS)
    
    def test_api_project_detail(self, client):
        """Test individual project API endpoint"""
        for project in PROJECTS:
            response = client.get(f'/api/projects/{project["id"]}')
            assert response.status_code == 200
            data = response.get_json()
            assert data['id'] == project['id']
    
    def test_api_project_detail_404(self, client):
        """Test 404 for nonexistent project in API"""
        response = client.get('/api/projects/nonexistent-xyz')
        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
    
    def test_api_publications(self, client):
        """Test publications API endpoint"""
        response = client.get('/api/publications')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == len(PUBLICATIONS)
    
    def test_api_about(self, client):
        """Test about API endpoint"""
        response = client.get('/api/about')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)
    
    def test_api_contact(self, client):
        """Test contact API endpoint"""
        response = client.get('/api/contact')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, dict)
    
    def test_api_contact_microservices(self, client):
        """Test contact microservice API endpoints"""
        services = ['research', 'speaking', 'consulting', 'collaboration']
        for service in services:
            response = client.get(f'/api/contact/{service}')
            assert response.status_code == 200, f"Contact API {service} failed"
            data = response.get_json()
            assert isinstance(data, dict)
    
    def test_api_contact_list(self, client):
        """Test contact services list API"""
        response = client.get('/api/contact/list')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == len(contact_services)
        
        # Validate structure of list items
        for item in data:
            assert 'id' in item
            assert 'endpoint' in item
            assert 'data' in item
    
    def test_api_contact_add(self, client):
        """Test adding a new contact microservice"""
        new_service = {
            'id': 'test_service',
            'endpoint': '/api/contact/test',
            'data': {'title': 'Test Service', 'description': 'Test description'}
        }
        
        initial_count = len(contact_services)
        
        response = client.post('/api/contact/add', 
                              data=json.dumps(new_service),
                              content_type='application/json')
        
        assert response.status_code == 201
        data = response.get_json()
        assert 'message' in data
        assert data['service']['id'] == 'test_service'
        assert data['total_services'] == initial_count + 1
    
    def test_api_contact_add_missing_fields(self, client):
        """Test validation for adding contact service"""
        incomplete_service = {'id': 'test'}
        
        response = client.post('/api/contact/add',
                              data=json.dumps(incomplete_service),
                              content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data


class TestLinkedListImplementation:
    """Test contact linked list implementation"""
    
    def test_linked_list_get(self):
        """Test getting nodes by ID"""
        node = contact_services.get('research')
        assert node is not None
        assert node.service_id == 'research'
        assert node.endpoint == '/api/contact/research'
    
    def test_linked_list_get_nonexistent(self):
        """Test getting nonexistent node"""
        node = contact_services.get('nonexistent-service-xyz')
        assert node is None
    
    def test_linked_list_traversal(self):
        """Test linked list traversal"""
        nodes = list(contact_services.traverse())
        assert len(nodes) > 0
        
        # Check that nodes are properly linked
        for i, node in enumerate(nodes[:-1]):
            assert node.next is not None
            assert node.next == nodes[i + 1]
        
        # Last node should have no next
        assert nodes[-1].next is None
    
    def test_linked_list_to_list(self):
        """Test converting linked list to Python list"""
        result = contact_services.to_list()
        assert isinstance(result, list)
        assert len(result) == len(contact_services)
        
        for item in result:
            assert 'id' in item
            assert 'endpoint' in item
            assert 'data' in item
    
    def test_linked_list_length(self):
        """Test linked list length"""
        assert len(contact_services) > 0
        assert len(contact_services) == contact_services.size

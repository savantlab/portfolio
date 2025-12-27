from flask import Flask, render_template, jsonify, request, session
import os
import json
from functools import wraps
from dotenv import load_dotenv
from contact_list import ContactLinkedList
import markdown

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))

# Authentication decorator
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        api_token = os.getenv('API_TOKEN')
        
        if not api_token:
            return jsonify({"error": "API authentication not configured"}), 500
        
        if not auth_header:
            return jsonify({"error": "Authorization header required"}), 401
        
        if not auth_header.startswith('Bearer '):
            return jsonify({"error": "Invalid authorization format. Use: Bearer <token>"}), 401
        
        token = auth_header.replace('Bearer ', '')
        if token != api_token:
            return jsonify({"error": "Invalid token"}), 403
        
        return f(*args, **kwargs)
    return decorated_function

# Load data from JSON files
def load_json_data(filename):
    """Load JSON data from data directory"""
    filepath = os.path.join(os.path.dirname(__file__), 'data', filename)
    with open(filepath, 'r') as f:
        return json.load(f)

# Load projects and publications
PROJECTS = load_json_data('projects.json')
PUBLICATIONS = load_json_data('publications.json')
ABOUT = load_json_data('about.json')
CONTACT = load_json_data('contact.json')
NAVIGATION = load_json_data('navigation.json')
READING_LIST = load_json_data('reading_list.json')

# Initialize contact microservices linked list
contact_services = ContactLinkedList()

# Load and add contact microservices to linked list
CONTACT_RESEARCH = load_json_data('contact_research.json')
contact_services.append('research', '/api/contact/research', CONTACT_RESEARCH)

CONTACT_SPEAKING = load_json_data('contact_speaking.json')
contact_services.append('speaking', '/api/contact/speaking', CONTACT_SPEAKING)

CONTACT_CONSULTING = load_json_data('contact_consulting.json')
contact_services.append('consulting', '/api/contact/consulting', CONTACT_CONSULTING)

CONTACT_COLLABORATION = load_json_data('contact_collaboration.json')
contact_services.append('collaboration', '/api/contact/collaboration', CONTACT_COLLABORATION)

# API Endpoints
@app.route("/api/projects")
@require_auth
def api_projects():
    """Get all projects as JSON"""
    return jsonify(PROJECTS)

@app.route("/api/projects/<project_id>")
@require_auth
def api_project_detail(project_id):
    """Get single project by ID as JSON"""
    project = next((p for p in PROJECTS if p["id"] == project_id), None)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(project)

@app.route("/api/publications")
@require_auth
def api_publications():
    """Get all publications as JSON"""
    return jsonify(PUBLICATIONS)

@app.route("/api/about")
@require_auth
def api_about():
    """Get about page data as JSON"""
    return jsonify(ABOUT)

@app.route("/api/contact")
@require_auth
def api_contact():
    """Get contact page data as JSON"""
    return jsonify(CONTACT)

@app.route("/api/navigation")
@require_auth
def api_navigation():
    """Get navigation links as JSON"""
    return jsonify(NAVIGATION)

@app.route("/nav")
def nav_component():
    """Serve navigation menu component as HTML microservice"""
    return render_template("nav_menu.html")

@app.route("/api/reading-list")
@require_auth
def api_reading_list():
    """Get all reading list items"""
    return jsonify(READING_LIST)

@app.route("/api/reading-list/add", methods=['POST'])
@require_auth
def api_reading_list_add():
    """Add a new item to reading list"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['title', 'categories']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields: title, categories"}), 400
    
    # Generate ID
    new_id = max([item['id'] for item in READING_LIST], default=0) + 1
    
    # Create new item
    new_item = {
        'id': new_id,
        'title': data['title'],
        'description': data.get('description'),
        'url': data.get('url'),
        'categories': data['categories'],
        'status': data.get('status', 'To Read')
    }
    
    READING_LIST.append(new_item)
    
    # Save to JSON file
    filepath = os.path.join(os.path.dirname(__file__), 'data', 'reading_list.json')
    with open(filepath, 'w') as f:
        json.dump(READING_LIST, f, indent=2)
    
    return jsonify({
        "message": "Item added successfully",
        "item": new_item,
        "total_items": len(READING_LIST)
    }), 201

@app.route("/api/reading-list/<int:item_id>", methods=['PUT'])
@require_auth
def api_reading_list_update(item_id):
    """Update an existing reading list item"""
    data = request.get_json()
    
    # Find the item
    item = next((i for i in READING_LIST if i['id'] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    # Update fields if provided
    if 'title' in data:
        item['title'] = data['title']
    if 'description' in data:
        item['description'] = data['description']
    if 'url' in data:
        item['url'] = data['url']
    if 'categories' in data:
        item['categories'] = data['categories']
    if 'status' in data:
        item['status'] = data['status']
    
    # Save to JSON file
    filepath = os.path.join(os.path.dirname(__file__), 'data', 'reading_list.json')
    with open(filepath, 'w') as f:
        json.dump(READING_LIST, f, indent=2)
    
    return jsonify({
        "message": "Item updated successfully",
        "item": item
    }), 200

@app.route("/api/contact/research")
@require_auth
def api_contact_research():
    """Get research participation microservice data"""
    return jsonify(CONTACT_RESEARCH)

@app.route("/api/contact/speaking")
@require_auth
def api_contact_speaking():
    """Get speaking engagements microservice data"""
    return jsonify(CONTACT_SPEAKING)

@app.route("/api/contact/consulting")
@require_auth
def api_contact_consulting():
    """Get technical consulting microservice data"""
    return jsonify(CONTACT_CONSULTING)

@app.route("/api/contact/collaboration")
@require_auth
def api_contact_collaboration():
    """Get collaboration microservice data"""
    return jsonify(CONTACT_COLLABORATION)

@app.route("/api/contact/list")
@require_auth
def api_contact_list():
    """Get the linked list of all contact microservices"""
    return jsonify(contact_services.to_list())

@app.route("/api/contact/add", methods=['POST'])
@require_auth
def api_contact_add():
    """Add a new contact microservice to the linked list"""
    data = request.get_json()
    service_id = data.get('id')
    endpoint = data.get('endpoint')
    service_data = data.get('data')
    
    if not all([service_id, endpoint, service_data]):
        return jsonify({"error": "Missing required fields: id, endpoint, data"}), 400
    
    contact_services.append(service_id, endpoint, service_data)
    return jsonify({
        "message": "Microservice added successfully",
        "service": {
            "id": service_id,
            "endpoint": endpoint
        },
        "total_services": len(contact_services)
    }), 201

# Web Routes
@app.route("/")
def index():
    return render_template("index.html", projects=PROJECTS, publications=PUBLICATIONS)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/contact/<service_id>")
def contact_service(service_id):
    """Render individual contact microservice page"""
    node = contact_services.get(service_id)
    if not node:
        return "Service not found", 404
    
    # Get previous and next nodes for navigation
    prev_node = None
    next_node = node.next
    
    current = contact_services.head
    while current and current.next:
        if current.next.service_id == service_id:
            prev_node = current
            break
        current = current.next
    
    return render_template(
        f"contact_{service_id}.html",
        service=node,
        prev_service=prev_node,
        next_service=next_node
    )

@app.route("/project/<project_id>")
def project_detail(project_id):
    project = next((p for p in PROJECTS if p["id"] == project_id), None)
    if not project:
        return "Project not found", 404
    return render_template("project.html", project=project)

@app.route("/journal")
def journal():
    return render_template("journal.html")

@app.route("/counterterrorism")
def counterterrorism():
    return render_template("counterterrorism.html")

@app.route("/reading")
def reading():
    return render_template("reading_list.html")

@app.route("/resume")
def resume():
    """Protected Palantir resume page with code validation"""
    return render_template("resume.html")

@app.route("/api/resume/validate", methods=['POST'])
def validate_resume_code():
    """Validate access code for resume"""
    data = request.get_json()
    code = data.get('code', '').strip()
    correct_code = os.getenv('RESUME_CODE', 'ARCHIMEDES2026')
    
    if code == correct_code:
        session['resume_access'] = True
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False, "error": "Invalid code"}), 403

@app.route("/api/resume/content")
@require_auth
def resume_content():
    """Get resume content (requires API authentication)"""
    # Read and convert markdown to HTML
    filepath = os.path.join(os.path.dirname(__file__), 'palantir_echo_resume_pitch.md')
    with open(filepath, 'r') as f:
        md_content = f.read()
    
    html_content = markdown.markdown(md_content, extensions=['fenced_code', 'tables', 'toc'])
    
    return jsonify({"content": html_content}), 200

@app.route("/healthz")
def healthz():
    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

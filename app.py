from flask import Flask, render_template, jsonify, request
import os
import json
from contact_list import ContactLinkedList

app = Flask(__name__)

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
def api_projects():
    """Get all projects as JSON"""
    return jsonify(PROJECTS)

@app.route("/api/projects/<project_id>")
def api_project_detail(project_id):
    """Get single project by ID as JSON"""
    project = next((p for p in PROJECTS if p["id"] == project_id), None)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(project)

@app.route("/api/publications")
def api_publications():
    """Get all publications as JSON"""
    return jsonify(PUBLICATIONS)

@app.route("/api/about")
def api_about():
    """Get about page data as JSON"""
    return jsonify(ABOUT)

@app.route("/api/contact")
def api_contact():
    """Get contact page data as JSON"""
    return jsonify(CONTACT)

@app.route("/api/navigation")
def api_navigation():
    """Get navigation links as JSON"""
    return jsonify(NAVIGATION)

@app.route("/api/contact/research")
def api_contact_research():
    """Get research participation microservice data"""
    return jsonify(CONTACT_RESEARCH)

@app.route("/api/contact/speaking")
def api_contact_speaking():
    """Get speaking engagements microservice data"""
    return jsonify(CONTACT_SPEAKING)

@app.route("/api/contact/consulting")
def api_contact_consulting():
    """Get technical consulting microservice data"""
    return jsonify(CONTACT_CONSULTING)

@app.route("/api/contact/collaboration")
def api_contact_collaboration():
    """Get collaboration microservice data"""
    return jsonify(CONTACT_COLLABORATION)

@app.route("/api/contact/list")
def api_contact_list():
    """Get the linked list of all contact microservices"""
    return jsonify(contact_services.to_list())

@app.route("/api/contact/add", methods=['POST'])
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


@app.route("/healthz")
def healthz():
    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

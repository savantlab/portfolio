from flask import Flask, render_template, jsonify
import os
import json

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

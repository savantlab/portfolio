from flask import Flask, render_template, request, jsonify
import os
import reading_list
import auth
import technical_implementation
import projects as projects_module

app = Flask(__name__)

PUBLICATIONS = [
    {
        "title": "The Surreal Art of Mental Rotation",
        "status": "Manuscript in Preparation",
        "description": "Challenges the prevailing allocentric model of spatial cognition using computational analysis of 50+ years of mental rotation research."
    },
    {
        "title": "Parallel Critiques: Analyzing Rhetorical Extremism",
        "status": "Technical Monograph in Development",
        "description": "Network co-occurrence analysis revealing how shared vocabulary masks fundamentally different conceptual architectures."
    }
]

@app.route("/")
def index():
    return render_template("index.html", projects=projects_module.get_all_projects(), publications=PUBLICATIONS)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/project/<project_id>")
def project_detail(project_id):
    project = projects_module.get_project(project_id)
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
    """Display the reading list page."""
    return render_template("reading_list.html")

@app.route("/healthz")
def healthz():
    return {"ok": True}

@app.route("/api/auth/token", methods=["POST"])
def request_token():
    """Request an authentication token via email."""
    data = request.get_json()
    
    if not data or "email" not in data:
        return jsonify({"error": "Email is required"}), 400
    
    email = data.get("email").strip().lower()
    token, error = auth.create_token(email)
    
    if error:
        return jsonify({"error": error}), 401
    
    # In production, send token via email
    # For now, return it directly (use with caution)
    return jsonify({
        "token": token,
        "message": "Token created. Use this token in your API requests.",
        "expires_in": f"{auth.TOKEN_EXPIRY_HOURS} hours"
    }), 201

@app.route("/api/auth/verify", methods=["POST"])
def verify_token_endpoint():
    """Verify (activate) a token."""
    data = request.get_json()
    
    if not data or "token" not in data:
        return jsonify({"error": "Token is required"}), 400
    
    token = data.get("token").strip()
    
    if not auth.mark_token_verified(token):
        return jsonify({"error": "Invalid token"}), 401
    
    return jsonify({
        "success": True,
        "message": "Token verified. You can now use it for API requests."
    })

@app.route("/api/reading-list", methods=["GET"])
@auth.require_auth
def get_reading_list():
    """Get all reading list items as JSON."""
    items = reading_list.get_all_items()
    return jsonify(items)

@app.route("/api/reading-list", methods=["POST"])
@auth.require_auth
def add_reading_item():
    """Add a new item to the reading list."""
    data = request.get_json()
    
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    
    item = reading_list.add_item(
        title=data.get("title"),
        url=data.get("url"),
        description=data.get("description"),
        category=data.get("category")
    )
    
    return jsonify(item), 201

@app.route("/api/reading-list/<int:item_id>", methods=["GET"])
@auth.require_auth
def get_reading_item(item_id):
    """Get a specific reading list item."""
    item = reading_list.get_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)

@app.route("/api/reading-list/<int:item_id>", methods=["PUT"])
@auth.require_auth
def update_reading_item(item_id):
    """Update a reading list item."""
    item = reading_list.get_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    data = request.get_json()
    updated_item = reading_list.update_item(item_id, **data)
    return jsonify(updated_item)

@app.route("/api/reading-list/<int:item_id>/toggle", methods=["POST"])
@auth.require_auth
def toggle_reading_item(item_id):
    """Toggle the completed status of a reading list item."""
    item = reading_list.toggle_completed(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)

@app.route("/api/reading-list/<int:item_id>", methods=["DELETE"])
@auth.require_auth
def delete_reading_item(item_id):
    """Delete a reading list item."""
    item = reading_list.get_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    reading_list.delete_item(item_id)
    return jsonify({"success": True})

@app.route("/api/technical-implementations", methods=["GET"])
def get_technical_implementations():
    """Get all technical implementation rows."""
    items = technical_implementation.get_all_implementations()
    return jsonify(items)

@app.route("/api/technical-implementations", methods=["POST"])
def add_technical_implementation():
    """Add a new technical implementation row item."""
    data = request.get_json()
    
    if not data or "title" not in data or "description" not in data:
        return jsonify({"error": "Title and description are required"}), 400
    
    try:
        item = technical_implementation.add_implementation(
            title=data.get("title"),
            description=data.get("description"),
            tech_stack=data.get("tech_stack", []),
            status=data.get("status", "Active")
        )
        return jsonify(item), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/technical-implementations/<int:item_id>", methods=["GET"])
def get_technical_implementation(item_id):
    """Get a specific technical implementation."""
    item = technical_implementation.get_implementation(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item)

@app.route("/api/technical-implementations/<int:item_id>", methods=["PUT"])
def update_technical_implementation(item_id):
    """Update a technical implementation."""
    item = technical_implementation.get_implementation(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    data = request.get_json()
    updated_item = technical_implementation.update_implementation(item_id, **data)
    return jsonify(updated_item)

@app.route("/api/technical-implementations/<int:item_id>", methods=["DELETE"])
def delete_technical_implementation(item_id):
    """Delete a technical implementation."""
    item = technical_implementation.get_implementation(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    technical_implementation.delete_implementation(item_id)
    return jsonify({"success": True})

@app.route("/api/projects", methods=["GET"])
def get_projects():
    """Get all projects."""
    return jsonify(projects_module.get_all_projects())

@app.route("/api/projects", methods=["POST"])
def add_project():
    """Add a new project."""
    data = request.get_json()
    
    required = ["title", "subtitle", "description", "tech", "highlights"]
    if not data or not all(k in data for k in required):
        return jsonify({"error": f"Required fields: {', '.join(required)}"}), 400
    
    try:
        project = projects_module.add_project(
            title=data.get("title"),
            subtitle=data.get("subtitle"),
            description=data.get("description"),
            tech=data.get("tech"),
            highlights=data.get("highlights"),
            github=data.get("github"),
            status=data.get("status", "Active"),
            image=data.get("image")
        )
        return jsonify(project), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/projects/<project_id>", methods=["GET"])
def get_project_api(project_id):
    """Get a specific project."""
    project = projects_module.get_project(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    return jsonify(project)

@app.route("/api/projects/<project_id>", methods=["PUT"])
def update_project(project_id):
    """Update a project."""
    project = projects_module.get_project(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    data = request.get_json()
    updated = projects_module.update_project(project_id, **data)
    return jsonify(updated)

@app.route("/api/projects/<project_id>", methods=["DELETE"])
def delete_project(project_id):
    """Delete a project."""
    project = projects_module.get_project(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    projects_module.delete_project(project_id)
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

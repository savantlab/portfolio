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
    """Load JSON data from flask_data directory"""
    filepath = os.path.join(os.path.dirname(__file__), 'flask_data', filename)
    with open(filepath, 'r') as f:
        return json.load(f)

# Load projects and publications
PROJECTS = load_json_data('projects.json')
PUBLICATIONS = load_json_data('publications.json')
ABOUT = load_json_data('about.json')
CONTACT = load_json_data('contact.json')
NAVIGATION = load_json_data('navigation.json')
READING_LIST = load_json_data('reading_list.json')
WRITING = load_json_data('writing.json')
PODCASTS = load_json_data('podcasts.json')

# Load Archimedes mental rotation research data from mental-rotation-research repository
ARCHIMEDES_DATASETS = {}
# Try mental-rotation-research repo first, fallback to Archimedes directory
mental_rotation_repo = os.path.join(os.path.expanduser('~'), 'mental-rotation-research')
archimedes_openalex_dir = os.path.join(mental_rotation_repo, 'data', 'archimedes_openalex')
archimedes_fallback_dir = os.path.join(os.path.expanduser('~'), 'Archimedes')

# Define datasets to load
# These are citation networks from foundational mental rotation papers
datasets_to_load = {
    'overlap_citations': 'overlap_citations_clean.json',  # Papers citing BOTH Shepard & Metzler (1971) AND Vandenberg & Kuse (1978)
    'shepard_metzler_citations': 'shepard_metzler_1971_citations_clean.json',  # Papers citing Shepard & Metzler (1971)
    'vandenberg_kuse_citations': 'vandenberg_kuse_1978_citations_clean.json',  # Papers citing Vandenberg & Kuse (1978)
}

for dataset_name, filename in datasets_to_load.items():
    try:
        # Try loading from mental-rotation-research repo first
        filepath = os.path.join(archimedes_openalex_dir, filename)
        if not os.path.exists(filepath):
            # Fallback to Archimedes directory
            filepath = os.path.join(archimedes_fallback_dir, filename)
        
        with open(filepath, 'r') as f:
            ARCHIMEDES_DATASETS[dataset_name] = json.load(f)
        print(f"Loaded {len(ARCHIMEDES_DATASETS[dataset_name])} papers from {dataset_name}")
    except FileNotFoundError:
        print(f"Warning: {filename} not found in mental-rotation-research or Archimedes directory")
        ARCHIMEDES_DATASETS[dataset_name] = []

# Create combined dataset (removing duplicates by DOI/title)
# Filter to only papers published after 1971 (papers that could cite Shepard & Metzler 1971)
# Exclude medical/clinical papers (pulmonary, radiology, etc.)
all_papers = []
seen_identifiers = set()

# Medical concepts to exclude
medical_exclude_concepts = {
    'medicine', 'radiology', 'surgery', 'pulmonary', 'clinical', 'medical',
    'patient', 'disease', 'therapy', 'diagnosis', 'pathology', 'anatomy',
    'computed tomography', 'ct scan', 'mri', 'imaging', 'radiography',
    'lung', 'heart', 'vascular', 'organ', 'tissue', 'cancer', 'tumor'
}

for dataset_name, papers in ARCHIMEDES_DATASETS.items():
    for paper in papers:
        # Filter: only papers from 1972 onwards
        paper_year = paper.get('year')
        if paper_year and paper_year < 1972:
            continue
        
        # Filter: exclude medical/clinical papers
        concepts = paper.get('concepts', [])
        concepts_lower = [c.lower() for c in concepts]
        if any(med_term in ' '.join(concepts_lower) for med_term in medical_exclude_concepts):
            continue
            
        # Use DOI as primary identifier, fall back to title
        identifier = paper.get('doi') or paper.get('title')
        if identifier and identifier not in seen_identifiers:
            seen_identifiers.add(identifier)
            # Add dataset source tag
            paper_copy = paper.copy()
            paper_copy['source_dataset'] = dataset_name
            all_papers.append(paper_copy)

ARCHIMEDES_PAPERS = all_papers
print(f"Total unique papers across all datasets (1972+): {len(ARCHIMEDES_PAPERS)}")

# Load Peterson citation network data
PETERSON_DATASETS = {}
petersson_citations_dir = os.path.join(os.path.expanduser('~'), 'Archimedes', 'peterson_citations')

petersson_datasets_to_load = {
    'peterson_network': 'jordan_peterson_network_cleaned.json',
    'peterson_papers': 'jordan_peterson_papers_cleaned.json',
    'maps_of_meaning': 'maps_of_meaning_citations_openalex.json',
    'maps_of_meaning_curated': 'maps_of_meaning_citations.json'
}

for dataset_name, filename in petersson_datasets_to_load.items():
    try:
        filepath = os.path.join(petersson_citations_dir, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)
            # Handle both metadata+papers structure and simple papers structure
            if isinstance(data, dict) and 'papers' in data:
                PETERSON_DATASETS[dataset_name] = data['papers']
            else:
                PETERSON_DATASETS[dataset_name] = data
        papers_count = len(PETERSON_DATASETS[dataset_name]) if isinstance(PETERSON_DATASETS[dataset_name], list) else 0
        print(f"Loaded {papers_count} papers from {dataset_name}")
    except FileNotFoundError:
        print(f"Warning: {filename} not found in {petersson_citations_dir}")
        PETERSON_DATASETS[dataset_name] = []
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        PETERSON_DATASETS[dataset_name] = []

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

@app.route("/api/podcasts")
def api_podcasts():
    """Get all podcast episodes with transcripts"""
    return jsonify(PODCASTS)

@app.route("/api/podcasts/<podcast_id>")
def api_podcast_detail(podcast_id):
    """Get single podcast episode by ID"""
    podcast = next((p for p in PODCASTS if p["id"] == podcast_id), None)
    if not podcast:
        return jsonify({"error": "Podcast not found"}), 404
    return jsonify(podcast)

# Writing API and pages
@app.route("/api/writing")
def api_writing_list():
    """Get list of writing samples"""
    return jsonify(WRITING)

@app.route("/api/writing/<post_id>")
def api_writing_detail(post_id):
    post = next((w for w in WRITING if w["id"] == post_id), None)
    if not post:
        return jsonify({"error": "Writing sample not found"}), 404
    return jsonify(post)

@app.route("/api/writing/upload", methods=['POST'])
@require_auth
def api_writing_upload():
    """Upload a .txt file as a new writing sample (multipart/form-data)"""
    file = request.files.get('file')
    title = request.form.get('title', '').strip() or 'Untitled'
    subtitle = request.form.get('subtitle', '').strip()
    tags = request.form.get('tags', '')
    tags_list = [t.strip() for t in tags.split(',') if t.strip()]

    if not file or not file.filename.lower().endswith('.txt'):
        return jsonify({"error": "A .txt file is required under form field 'file'"}), 400

    # Create ID slug
    slug = title.lower().replace(' ', '-').replace('/', '-').replace("'", "")
    idx = 1
    base_slug = slug or 'writing'
    existing_ids = {w['id'] for w in WRITING}
    while slug in existing_ids:
        idx += 1
        slug = f"{base_slug}-{idx}"

    # Save file into flask_data/writing_files/
    files_dir = os.path.join(os.path.dirname(__file__), 'flask_data', 'writing_files')
    os.makedirs(files_dir, exist_ok=True)
    filepath = os.path.join(files_dir, f"{slug}.txt")
    file.save(filepath)

    # Read text content
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # Build record
    new_post = {
        'id': slug,
        'title': title,
        'subtitle': subtitle,
        'status': 'In Development',
        'tags': tags_list,
        'author': 'Stephanie King',
        'created': None,
        'description': subtitle or title,
        'text': text
    }

    # Update in-memory and persist
    WRITING.append(new_post)
    outpath = os.path.join(os.path.dirname(__file__), 'flask_data', 'writing.json')
    with open(outpath, 'w') as f:
        json.dump(WRITING, f, indent=2)

    return jsonify({"message": "Writing uploaded", "id": slug}), 201

@app.route("/writing")
def writing_list_page():
    return render_template("writing.html", writing=WRITING)

@app.route("/writing/<post_id>")
def writing_detail_page(post_id):
    post = next((w for w in WRITING if w["id"] == post_id), None)
    if not post:
        return "Writing sample not found", 404
    return render_template("writing_detail.html", post=post)

@app.route("/nav")
def nav_component():
    """Serve navigation menu component as HTML microservice"""
    return render_template("nav_menu.html")

@app.route("/api/reading-list")
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
    filepath = os.path.join(os.path.dirname(__file__), 'flask_data', 'reading_list.json')
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
    filepath = os.path.join(os.path.dirname(__file__), 'flask_data', 'reading_list.json')
    with open(filepath, 'w') as f:
        json.dump(READING_LIST, f, indent=2)
    
    return jsonify({
        "message": "Item updated successfully",
        "item": item
    }), 200

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

# Data Population Endpoints
@app.route("/api/projects/<project_id>", methods=['DELETE'])
@require_auth
def api_project_delete(project_id):
    """Delete a project by ID"""
    global PROJECTS
    
    # Find and remove the project
    project = next((p for p in PROJECTS if p['id'] == project_id), None)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    PROJECTS = [p for p in PROJECTS if p['id'] != project_id]
    
    # Save to JSON file
    filepath = os.path.join(os.path.dirname(__file__), 'flask_data', 'projects.json')
    with open(filepath, 'w') as f:
        json.dump(PROJECTS, f, indent=2)
    
    return jsonify({
        "message": "Project deleted successfully",
        "deleted_project": project,
        "remaining_projects": len(PROJECTS)
    }), 200

@app.route("/api/projects/populate", methods=['POST'])
@require_auth
def api_projects_populate():
    """Populate/replace projects data"""
    global PROJECTS
    data = request.get_json()
    
    if not isinstance(data, list):
        return jsonify({"error": "Data must be an array of projects"}), 400
    
    PROJECTS = data
    filepath = os.path.join(os.path.dirname(__file__), 'flask_data', 'projects.json')
    with open(filepath, 'w') as f:
        json.dump(PROJECTS, f, indent=2)
    
    return jsonify({
        "message": "Projects populated successfully",
        "total_projects": len(PROJECTS)
    }), 200

@app.route("/api/publications/populate", methods=['POST'])
@require_auth
def api_publications_populate():
    """Populate/replace publications data"""
    global PUBLICATIONS
    data = request.get_json()
    
    if not isinstance(data, list):
        return jsonify({"error": "Data must be an array of publications"}), 400
    
    PUBLICATIONS = data
    filepath = os.path.join(os.path.dirname(__file__), 'flask_data', 'publications.json')
    with open(filepath, 'w') as f:
        json.dump(PUBLICATIONS, f, indent=2)
    
    return jsonify({
        "message": "Publications populated successfully",
        "total_publications": len(PUBLICATIONS)
    }), 200

@app.route("/api/about/populate", methods=['POST'])
@require_auth
def api_about_populate():
    """Populate/replace about page data"""
    global ABOUT
    data = request.get_json()
    
    if not isinstance(data, dict):
        return jsonify({"error": "Data must be an object"}), 400
    
    ABOUT = data
    filepath = os.path.join(os.path.dirname(__file__), 'flask_data', 'about.json')
    with open(filepath, 'w') as f:
        json.dump(ABOUT, f, indent=2)
    
    return jsonify({
        "message": "About page populated successfully"
    }), 200

@app.route("/api/contact/populate", methods=['POST'])
@require_auth
def api_contact_populate():
    """Populate/replace contact page data"""
    global CONTACT
    data = request.get_json()
    
    if not isinstance(data, dict):
        return jsonify({"error": "Data must be an object"}), 400
    
    CONTACT = data
    filepath = os.path.join(os.path.dirname(__file__), 'flask_data', 'contact.json')
    with open(filepath, 'w') as f:
        json.dump(CONTACT, f, indent=2)
    
    return jsonify({
        "message": "Contact page populated successfully"
    }), 200

@app.route("/api/navigation/populate", methods=['POST'])
@require_auth
def api_navigation_populate():
    """Populate/replace navigation data"""
    global NAVIGATION
    data = request.get_json()
    
    if not isinstance(data, dict):
        return jsonify({"error": "Data must be an object"}), 400
    
    NAVIGATION = data
    filepath = os.path.join(os.path.dirname(__file__), 'flask_data', 'navigation.json')
    with open(filepath, 'w') as f:
        json.dump(NAVIGATION, f, indent=2)
    
    return jsonify({
        "message": "Navigation populated successfully"
    }), 200

@app.route("/api/contact/research/populate", methods=['POST'])
@require_auth
def api_contact_research_populate():
    """Populate/replace contact research microservice data"""
    global CONTACT_RESEARCH
    data = request.get_json()
    
    if not isinstance(data, dict):
        return jsonify({"error": "Data must be an object"}), 400
    
    CONTACT_RESEARCH = data
    filepath = os.path.join(os.path.dirname(__file__), 'flask_data', 'contact_research.json')
    with open(filepath, 'w') as f:
        json.dump(CONTACT_RESEARCH, f, indent=2)
    
    # Update linked list
    node = contact_services.get('research')
    if node:
        node.data = CONTACT_RESEARCH
    
    return jsonify({
        "message": "Contact research populated successfully"
    }), 200

@app.route("/api/contact/speaking/populate", methods=['POST'])
@require_auth
def api_contact_speaking_populate():
    """Populate/replace contact speaking microservice data"""
    global CONTACT_SPEAKING
    data = request.get_json()
    
    if not isinstance(data, dict):
        return jsonify({"error": "Data must be an object"}), 400
    
    CONTACT_SPEAKING = data
    filepath = os.path.join(os.path.dirname(__file__), 'flask_data', 'contact_speaking.json')
    with open(filepath, 'w') as f:
        json.dump(CONTACT_SPEAKING, f, indent=2)
    
    # Update linked list
    node = contact_services.get('speaking')
    if node:
        node.data = CONTACT_SPEAKING
    
    return jsonify({
        "message": "Contact speaking populated successfully"
    }), 200

@app.route("/api/contact/consulting/populate", methods=['POST'])
@require_auth
def api_contact_consulting_populate():
    """Populate/replace contact consulting microservice data"""
    global CONTACT_CONSULTING
    data = request.get_json()
    
    if not isinstance(data, dict):
        return jsonify({"error": "Data must be an object"}), 400
    
    CONTACT_CONSULTING = data
    filepath = os.path.join(os.path.dirname(__file__), 'flask_data', 'contact_consulting.json')
    with open(filepath, 'w') as f:
        json.dump(CONTACT_CONSULTING, f, indent=2)
    
    # Update linked list
    node = contact_services.get('consulting')
    if node:
        node.data = CONTACT_CONSULTING
    
    return jsonify({
        "message": "Contact consulting populated successfully"
    }), 200

@app.route("/api/contact/collaboration/populate", methods=['POST'])
@require_auth
def api_contact_collaboration_populate():
    """Populate/replace contact collaboration microservice data"""
    global CONTACT_COLLABORATION
    data = request.get_json()
    
    if not isinstance(data, dict):
        return jsonify({"error": "Data must be an object"}), 400
    
    CONTACT_COLLABORATION = data
    filepath = os.path.join(os.path.dirname(__file__), 'flask_data', 'contact_collaboration.json')
    with open(filepath, 'w') as f:
        json.dump(CONTACT_COLLABORATION, f, indent=2)
    
    # Update linked list
    node = contact_services.get('collaboration')
    if node:
        node.data = CONTACT_COLLABORATION
    
    return jsonify({
        "message": "Contact collaboration populated successfully"
    }), 200

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

@app.route("/archimedes")
def archimedes():
    """Archimedes mental rotation research dashboard"""
    return render_template("archimedes.html", papers=ARCHIMEDES_PAPERS)

@app.route("/archimedes/dashboard")
def archimedes_dashboard():
    """Archimedes visualization dashboard"""
    return render_template("archimedes_dashboard.html")

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
def resume_content():
    """Get resume content (requires session authentication via code validation)"""
    # Check if user has validated access code
    if not session.get('resume_access'):
        return jsonify({"error": "Access code required"}), 403
    
    # Read and convert markdown to HTML
    filepath = os.path.join(os.path.dirname(__file__), 'palantir_echo_resume_pitch.md')
    with open(filepath, 'r') as f:
        md_content = f.read()
    
    html_content = markdown.markdown(md_content, extensions=['fenced_code', 'tables', 'toc'])
    
    return jsonify({"content": html_content}), 200

@app.route("/api/archimedes/papers")
@require_auth
def api_archimedes_papers():
    """Get all mental rotation research papers (combined, deduplicated)"""
    return jsonify(ARCHIMEDES_PAPERS)

@app.route("/api/archimedes/datasets")
@require_auth
def api_archimedes_datasets():
    """Get list of available datasets with counts"""
    dataset_info = {
        name: {
            'count': len(papers),
            'name': name.replace('_', ' ').title()
        }
        for name, papers in ARCHIMEDES_DATASETS.items()
    }
    dataset_info['all_papers'] = {
        'count': len(ARCHIMEDES_PAPERS),
        'name': 'All Papers (Deduplicated)'
    }
    return jsonify(dataset_info)

@app.route("/api/archimedes/dataset/<dataset_name>")
@require_auth
def api_archimedes_dataset(dataset_name):
    """Get papers from a specific dataset"""
    if dataset_name not in ARCHIMEDES_DATASETS:
        return jsonify({"error": "Dataset not found"}), 404
    return jsonify(ARCHIMEDES_DATASETS[dataset_name])

# Peterson Citation Network API Routes
@app.route("/api/archimedes/peterson/network")
@require_auth
def api_peterson_network():
    """Get Jordan Peterson citation network (cleaned, realistic statistics)"""
    return jsonify({
        "metadata": {
            "description": "Jordan B. Peterson citation network with false positives removed",
            "total_papers": len(PETERSON_DATASETS.get('peterson_network', [])),
            "note": "Cleaned to remove methodology papers and false positives",
            "average_citations": 1104,
            "median_citations": 34
        },
        "papers": PETERSON_DATASETS.get('peterson_network', [])
    })

@app.route("/api/archimedes/peterson/papers")
@require_auth
def api_peterson_papers():
    """Get verified Peterson authored papers"""
    return jsonify({
        "metadata": {
            "description": "Papers with Jordan B. Peterson as author",
            "total_papers": len(PETERSON_DATASETS.get('peterson_papers', [])),
            "note": "Only 1 confirmed Peterson paper found in OpenAlex: goal-setting intervention study (2015)"
        },
        "papers": PETERSON_DATASETS.get('peterson_papers', [])
    })

@app.route("/api/archimedes/peterson/maps-of-meaning")
@require_auth
def api_maps_of_meaning():
    """Get papers related to Maps of Meaning: The Architecture of Belief (1999)"""
    return jsonify({
        "metadata": {
            "description": "Papers citing or related to Jordan Peterson's Maps of Meaning",
            "total_papers": len(PETERSON_DATASETS.get('maps_of_meaning_curated', [])),
            "subject": "Meaning-making, mythology, psychology, archetypal theory"
        },
        "papers": PETERSON_DATASETS.get('maps_of_meaning_curated', [])
    })

@app.route("/api/archimedes/peterson/citations")
@require_auth
def api_peterson_citations():
    """Get all Peterson-related citations and datasets"""
    return jsonify({
        "metadata": {
            "description": "Jordan B. Peterson citation network and related datasets",
            "datasets": {
                "peterson_network": len(PETERSON_DATASETS.get('peterson_network', [])),
                "peterson_papers": len(PETERSON_DATASETS.get('peterson_papers', [])),
                "maps_of_meaning": len(PETERSON_DATASETS.get('maps_of_meaning', [])),
                "maps_of_meaning_curated": len(PETERSON_DATASETS.get('maps_of_meaning_curated', []))
            }
        },
        "endpoints": {
            "network": "/api/archimedes/peterson/network",
            "papers": "/api/archimedes/peterson/papers",
            "maps_of_meaning": "/api/archimedes/peterson/maps-of-meaning"
        }
    })

@app.route("/archimedes/peterson")
def archimedes_peterson():
    """Peterson citations dashboard"""
    return render_template(
        "archimedes_peterson.html",
        peterson_network=PETERSON_DATASETS.get('peterson_network', []),
        maps_of_meaning=PETERSON_DATASETS.get('maps_of_meaning_curated', [])
    )

# Project Gorgon: Peterson Podcast Episodes
@app.route("/gorgon/peterson-podcasts.json")
def gorgon_peterson_podcasts():
    """Password-protected Peterson podcast episode list (Project Gorgon)"""
    password = request.args.get('password') or request.headers.get('X-Gorgon-Password')
    correct_password = os.getenv('GORGON_PASSWORD', 'ARCHIMEDES2026')
    
    if password != correct_password:
        return jsonify({
            "error": "Access denied",
            "message": "Valid password required",
            "hint": "Use ?password=YOUR_PASSWORD or X-Gorgon-Password header"
        }), 403
    
    filepath = os.path.join(os.path.dirname(__file__), 'flask_data', 'peterson-podcasts.json')
    with open(filepath, 'r') as f:
        episodes = json.load(f)
    
    return jsonify({
        "project": "GORGON",
        "description": "Peterson podcast episode URLs for transcript analysis",
        "total_episodes": len(episodes),
        "episodes": episodes
    })

@app.route("/healthz")
def healthz():
    return {"ok": True}

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors"""
    return render_template("500.html"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

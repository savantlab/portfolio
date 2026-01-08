#!/usr/bin/env python3
"""
Enrich project data with comprehensive tech stack information from GitHub
"""
import json
import requests
import time

def get_repo_languages(repo_url):
    """Get language breakdown from GitHub repo"""
    # Extract owner/repo from URL
    parts = repo_url.rstrip('/').split('/')
    owner, repo = parts[-2], parts[-1]
    
    api_url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            languages = response.json()
            # Convert bytes to percentages and sort
            total = sum(languages.values())
            lang_list = [
                lang for lang, bytes_count in 
                sorted(languages.items(), key=lambda x: x[1], reverse=True)
            ]
            return lang_list
        else:
            print(f"  Warning: Could not fetch languages for {repo}")
            return None
    except Exception as e:
        print(f"  Error: {e}")
        return None

def get_python_frameworks(repo_url):
    """Get Python frameworks from requirements.txt"""
    parts = repo_url.rstrip('/').split('/')
    owner, repo = parts[-2], parts[-1]
    
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/requirements.txt"
    
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            reqs = [line.split('==')[0].split('>=')[0].split('[')[0].strip() 
                   for line in response.text.split('\n') 
                   if line and not line.startswith('#')]
            
            # Major frameworks to highlight
            framework_map = {
                'flask': 'Flask', 'django': 'Django', 'fastapi': 'FastAPI',
                'pandas': 'Pandas', 'numpy': 'NumPy', 'scikit-learn': 'Scikit-learn',
                'tensorflow': 'TensorFlow', 'pytorch': 'PyTorch', 'torch': 'PyTorch',
                'sqlalchemy': 'SQLAlchemy', 'celery': 'Celery', 'redis': 'Redis',
                'gunicorn': 'Gunicorn', 'pytest': 'Pytest', 'requests': 'Requests'
            }
            
            frameworks = []
            for req in reqs:
                req_lower = req.lower()
                if req_lower in framework_map:
                    frameworks.append(framework_map[req_lower])
            
            return frameworks
    except:
        pass
    return []

def enrich_projects():
    """Enrich all projects with GitHub language data"""
    with open('flask_data/projects.json', 'r') as f:
        projects = json.load(f)
    
    print(f"Enriching {len(projects)} projects...\n")
    
    for i, project in enumerate(projects, 1):
        print(f"{i}. {project['title']}")
        
        if project.get('github'):
            languages = get_repo_languages(project['github'])
            
            if languages:
                project['tech'] = languages
                print(f"   Languages: {', '.join(languages)}")
                
                # Get Python frameworks if applicable
                if 'Python' in languages:
                    frameworks = get_python_frameworks(project['github'])
                    if frameworks:
                        project['frameworks'] = frameworks
                        print(f"   Frameworks: {', '.join(frameworks)}")
                
                # Update highlights with language info
                project['highlights'] = [
                    h for h in project.get('highlights', []) 
                    if not h.startswith('Language:') and not h.startswith('Frameworks:')
                ]
                project['highlights'].insert(1, f"Language: {languages[0]}")
                
                # Add framework highlight if available
                if project.get('frameworks'):
                    frameworks_str = ', '.join(project['frameworks'][:3])
                    project['highlights'].insert(2, f"Frameworks: {frameworks_str}")
                
                # Add comprehensive description if missing details
                if len(project.get('description', '')) < 100:
                    tech_summary = ', '.join(languages[:3])
                    project['description'] = f"{project.get('subtitle', '')} Built with {tech_summary}."
            
            # Rate limit: sleep between requests
            time.sleep(0.5)
        
        print()
    
    # Save enriched data
    with open('flask_data/projects.json', 'w') as f:
        json.dump(projects, f, indent=2)
    
    print("✓ Projects enriched successfully!")
    print(f"Saved to: flask_data/projects.json")

if __name__ == '__main__':
    enrich_projects()

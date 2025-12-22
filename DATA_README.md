# Data Directory

## Overview
This application loads project and publication data from JSON files in the `data/` directory.

## Structure
```
data/
├── projects.json      # All project data
└── publications.json  # All publication data
```

## Deployment Strategy

### Main Branch
- `data/` directory is **gitignored**
- Contains code that loads from JSON
- JSON files exist locally for development
- Not committed to version control

### Deploy Branch
- `data/` directory **is committed**
- Contains both code AND data files
- Production server uses this branch

## Local Development

1. Keep your JSON files in `data/` directory locally
2. Edit them as needed for testing
3. Changes to JSON won't be committed to main
4. When ready to deploy, merge main to deploy and add JSON files there

## Updating Project Data

To update projects or publications:

1. Edit JSON files locally in `data/`
2. Test changes locally
3. When ready for production:
   ```bash
   git checkout deploy
   git merge main
   # Copy updated JSON files
   cp data/*.json data/
   git add data/
   git commit -m "Update project data"
   git push origin deploy
   ```

## JSON Schema

### projects.json
```json
[
  {
    "id": "project-slug",
    "title": "Project Title",
    "subtitle": "Brief subtitle",
    "description": "Full description",
    "tech": ["Tech1", "Tech2"],
    "highlights": ["Highlight 1", "Highlight 2"],
    "github": "https://github.com/...",
    "status": "Status",
    "image": "image.png or null"
  }
]
```

### publications.json
```json
[
  {
    "title": "Publication Title",
    "status": "Status",
    "description": "Description"
  }
]
```

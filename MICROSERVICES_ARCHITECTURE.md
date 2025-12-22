# Microservices Architecture Strategy

## Overview
This portfolio application demonstrates a microservices-oriented architecture where data and presentation are decoupled, services are rendered via REST API, and deployment follows modern CI/CD practices.

## Architecture Principles

### 1. Data Separation
- **Data Layer**: JSON files in `data/` directory (deploy branch only)
- **API Layer**: REST endpoints expose data as JSON
- **Presentation Layer**: Frontend fetches from API and renders

### 2. Service-Oriented Design
Each functional area is modular and can be deployed independently:
- **Projects Service**: `/api/projects`, `/api/projects/<id>`
- **Publications Service**: `/api/publications`
- **Blog Service**: Blog module (blog.py)
- **Technical Implementation Service**: Research tracking

### 3. Deployment Strategy

#### Branch Strategy
```
main (development)
  ↓
  - Code only (no data files)
  - REST API implementations
  - Frontend that consumes APIs
  - CI/CD pipelines
  - Automated tests
  
deploy (production)
  ↓
  - Merges from main
  - Includes data files (data/*.json)
  - Triggers production deployment
  - Runs on savantlab.org
```

#### CI/CD Pipeline
```
Push to main
  ↓
GitHub Actions Test Pipeline
  - Lint checking
  - Data structure validation
  - Route testing
  - Security scanning
  ↓
Manual deploy (./deploy.sh)
  ↓
Merge main → deploy
Add JSON data files
  ↓
Push to deploy
  ↓
GitHub Actions Deploy Workflow
  - SSH to production server
  - Pull latest code
  - Install dependencies
  - Restart services
  ↓
Live at savantlab.org
```

## Current Microservices

### 1. Projects API Service
**Endpoints**:
- `GET /api/projects` - List all projects
- `GET /api/projects/<id>` - Get single project

**Data Source**: `data/projects.json`

**Frontend Integration**: JavaScript fetch → Dynamic rendering

### 2. Publications API Service
**Endpoints**:
- `GET /api/publications` - List all publications

**Data Source**: `data/publications.json`

### 3. Blog Service
**Module**: `blog.py`
**Database**: SQLite via `database.py`
**Models**: `models.py`

### 4. Technical Implementation Tracker
**Module**: `technical_implementation.py`
**Purpose**: Research progress tracking

## Benefits of This Architecture

### Scalability
- Each service can scale independently
- API-first design allows multiple frontends (web, mobile, CLI)
- Easy to add new services without touching existing code

### Maintainability
- Clear separation of concerns
- Data changes don't require code deployment
- Easy to test each service in isolation

### Security
- API layer provides single point for authentication/authorization
- Data validation happens at API level
- Frontend never directly accesses data files

### Developer Experience
- Local development without production data
- JSON files make it easy to update content
- Automated testing catches issues before deployment

## Future Microservice Candidates

### Research Data Service
```
GET /api/research/mental-rotation
GET /api/research/papers
GET /api/research/authors
```

### Portfolio Analytics Service
```
GET /api/analytics/projects
GET /api/analytics/visitors
```

### Contact Form Service
```
POST /api/contact
```

### Resume Service
```
GET /api/resume
GET /api/resume/skills
GET /api/resume/experience
```

## Implementation Checklist

- [x] REST API for projects
- [x] REST API for publications
- [x] JSON data separation
- [x] CI/CD test pipeline
- [x] Automated deployment script
- [ ] Authentication for POST endpoints
- [ ] Rate limiting on API endpoints
- [ ] API documentation (OpenAPI/Swagger)
- [ ] Service health checks
- [ ] Monitoring and logging

## Testing Strategy

### Unit Tests
Test each service module independently

### Integration Tests
Test API endpoints with test data

### End-to-End Tests
Test full user workflows

### Current Test Coverage
- Flask app imports
- Data structure validation
- Route availability
- Project detail pages

## Documentation

- `DATA_README.md` - Data directory structure and deployment
- `CI_CD_WORKFLOW.md` - Deployment workflow guide
- `DEPLOYMENT_CHECKLIST.md` - Pre-deployment verification
- `MICROSERVICES_ARCHITECTURE.md` - This document

## Example: Adding a New Microservice

1. **Create service module** (e.g., `analytics.py`)
2. **Define API endpoints** in `app.py`:
   ```python
   @app.route("/api/analytics/projects")
   def api_analytics_projects():
       # Service logic
       return jsonify(data)
   ```
3. **Add data file** (if needed) to `data/`
4. **Write tests** in test pipeline
5. **Deploy** via standard workflow

## Monitoring Production

- **Health Check**: `GET /healthz`
- **GitHub Actions**: Monitor deployment status
- **Server Logs**: `tail -f /flask/gunicorn.log`
- **API Response Times**: Future monitoring service

## Related Projects

This architecture is inspired by:
- **Tax Budget Allocator**: Multi-container orchestration with Redis, Celery
- **Mad Scientist AI**: FastAPI microservices with Cloudflare AI
- **Mental Rotation Pipeline**: d6tflow orchestration, modular data processing

---

**This portfolio itself demonstrates the microservices architecture it describes.**

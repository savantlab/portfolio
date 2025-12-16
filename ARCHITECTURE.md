# Savantlab Portfolio - Architecture & Deployment Strategy

## Executive Summary

This repository implements a streamlined branching strategy that eliminates staging environments by separating production-ready code (main) from development/deployment infrastructure (deploy). This approach reduces operational complexity while maintaining clean code separation.

## Repository Structure

### Main Branch (Production)
The `main` branch contains only the essential application code optimized for production deployment:
- `app.py` - Flask application with routes and business logic
- `requirements.txt` - Core dependencies only
- `templates/` - HTML templates
- `static/` - CSS and JavaScript assets
- `README.md` - User documentation
- `.gitignore` - Git configuration

**Deployment**: Direct from main to production. No staging required.

### Deploy Branch (Development & Deployment)
The `deploy` branch contains the full development environment and deployment infrastructure:
- All production files from main
- `flask_driver_runner.py` - Flask + Chromedriver lifecycle manager
- `reading_list_cli.py` - Command-line interface for reading list management
- `auth.py` - Authentication module
- `reading_list.py` - Reading list business logic
- `setup_chromedriver.py` - Automated chromedriver setup
- `chromedriver_config.py` - Chromedriver configuration
- `run.sh` - Automated startup script with authentication
- `READING_LIST_API.md` - API documentation
- `.env.development` - Development configuration

**Purpose**: 
- Local development and testing
- Integration testing with full stack
- Staging before promotion to main
- Documentation of deployment infrastructure

## Development Workflow

### For Production (Main Branch)
1. Code is kept minimal and focused
2. Only essential files are tracked
3. Direct deployment to production
4. No intermediate staging environment needed

### For Development (Deploy Branch)
1. Full development environment with all tools
2. Testing and integration verification
3. Documentation of deployment procedures
4. Infrastructure as code (startup scripts, configuration)

## Promotion Path

```
Feature Development (deploy)
            ↓
Integration Testing (deploy)
            ↓
Code Review & Testing (deploy)
            ↓
Cherry-pick/Merge to main
            ↓
Production Deployment (main)
```

## Benefits of This Strategy

1. **Simplified Deployments**: No staging environment required. Main is always production-ready.
2. **Clean Git History**: Main branch contains only essential code, making audits easier.
3. **Development Isolation**: All development tooling kept separate in deploy branch.
4. **Clear Separation of Concerns**: Production code vs. deployment infrastructure.
5. **Reduced Operational Overhead**: Eliminates the need for environment parity between staging and production.
6. **Faster Iteration**: Deploy branch can be used for experimentation without affecting main.

## Key Technologies

- **Flask**: Web framework for the portfolio application
- **Selenium + Chromedriver**: Browser automation (deploy branch only)
- **Authentication**: Token-based API authentication with email verification
- **Reading List API**: RESTful API with CRUD operations for reading items

## Security Considerations

- Sensitive files (.env tokens) excluded from version control via .gitignore
- Credentials never stored in main branch
- Deploy branch contains setup scripts but no hardcoded secrets
- Authentication tokens generated at runtime, not committed

## Getting Started

### Production (Main)
```bash
pip install -r requirements.txt
python app.py
```

### Development (Deploy)
```bash
git checkout deploy
pip install -r requirements.txt
./run.sh  # Automated setup and authentication
```

## Future Enhancements

- CI/CD pipeline to automate promotion from deploy to main
- Automated testing gates before main promotion
- Container support for consistent deployment across environments
- Remote configuration management for production environment variables

## Conclusion

This architecture reduces deployment complexity by eliminating the staging/production environment gap. The deploy branch serves as both a development environment and documentation of the deployment infrastructure, while main remains a clean, production-focused representation of the application.

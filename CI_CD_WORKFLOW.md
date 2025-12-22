# CI/CD Workflow

## Quick Start

### When Pushing Changes to Main

1. **Make your changes locally**
2. **Commit to main branch**
   ```bash
   git add <files>
   git commit -m "Your commit message"
   git push origin main
   ```
3. **Wait for GitHub Actions Test Pipeline** ✓
   - Check: https://github.com/savantlab/portfolio/actions
   - Tests run automatically on every push to main
   - Must pass before deploying

4. **Deploy to production** (only after tests pass)
   ```bash
   ./deploy.sh
   ```
   Or manually:
   ```bash
   git checkout deploy
   git merge main
   git push origin deploy
   ```

## The Pipeline

### Main Branch → Test Pipeline (Automatic)
Every push to `main` triggers automated testing:
- ✓ Syntax checking (flake8)
- ✓ Code formatting (black)
- ✓ Flask app validation
- ✓ Route testing
- ✓ Data structure validation
- ✓ Security scanning

**Location**: `.github/workflows/test.yml`

### Deploy Branch → Production Deployment (Automatic)
Every push to `deploy` triggers deployment to savantlab.org:
- Pulls latest code on server
- Installs dependencies
- Restarts gunicorn
- Site goes live

**Location**: `.github/workflows/deploy.yml`

## Best Practices

### ✅ DO
- Push to `main` frequently with small commits
- Wait for tests to pass before deploying
- Use `./deploy.sh` for safe deployments
- Review git diff before deploying
- Test locally before pushing

### ❌ DON'T
- Push directly to `deploy` branch
- Deploy without running tests
- Commit sensitive data (passwords, API keys)
- Skip the checklist

## Files

- `DEPLOYMENT_CHECKLIST.md` - Detailed deployment checklist
- `deploy.sh` - Automated deployment script with safety checks
- `.github/workflows/test.yml` - Test pipeline configuration
- `.github/workflows/deploy.yml` - Deployment pipeline configuration

## Typical Workflow

```bash
# 1. Make changes
vim app.py

# 2. Test locally (optional but recommended)
python app.py
# Visit http://localhost:5001

# 3. Commit and push to main
git add app.py
git commit -m "Add new feature"
git push origin main

# 4. Wait for tests (watch GitHub Actions)
# ✓ All tests pass

# 5. Deploy to production
./deploy.sh
# Answer "yes" when prompted

# 6. Verify at https://savantlab.org
```

## Monitoring

- **GitHub Actions**: https://github.com/savantlab/portfolio/actions
- **Production Site**: https://savantlab.org
- **Server Logs**: SSH to server, `tail -f /flask/gunicorn.log`

## Troubleshooting

### Tests Failing on GitHub Actions?
```bash
# Run tests locally to debug
python3 -c "from app import app; print('OK')"
```

### Deploy Not Working?
```bash
# Check current branches
git branch -a

# Check GitHub Actions status
# Visit https://github.com/savantlab/portfolio/actions

# Manual server check (if needed)
# SSH to server and check logs
```

### Need to Rollback?
```bash
git checkout deploy
git reset --hard HEAD~1  # Go back one commit
git push origin deploy --force
```

## Summary

- **`main` branch** = Development, auto-tested
- **`deploy` branch** = Production, auto-deployed
- **Workflow**: main → tests pass → deploy → production

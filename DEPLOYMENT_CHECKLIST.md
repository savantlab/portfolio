# Deployment Checklist

Follow this checklist before deploying to production.

## Pre-Deployment Checklist

### 1. Code Quality
- [ ] All code changes reviewed
- [ ] No syntax errors or linting issues
- [ ] Code follows project conventions
- [ ] No hardcoded secrets or sensitive data

### 2. Testing
- [ ] Flask app imports successfully
- [ ] All routes return expected status codes
- [ ] Project data structure is valid
- [ ] Required files present (requirements.txt, app.py, templates/, static/)
- [ ] Local testing completed (`python app.py`)

### 3. GitHub Actions
- [ ] Push to `main` branch
- [ ] Wait for Test Pipeline to pass (check GitHub Actions tab)
- [ ] Review test results and fix any issues
- [ ] All tests green ✓

### 4. Pre-Deploy Verification
- [ ] Review git diff between main and deploy
- [ ] Confirm no unintended changes
- [ ] Backup current production state (optional but recommended)

### 5. Deployment
- [ ] Merge main into deploy branch
- [ ] Monitor GitHub Actions deployment workflow
- [ ] Verify deployment completes successfully

### 6. Post-Deployment
- [ ] Visit https://savantlab.org and verify site loads
- [ ] Test key routes:
  - [ ] Homepage (/)
  - [ ] Projects page with new additions
  - [ ] Individual project pages
  - [ ] About, Contact, Journal pages
- [ ] Check browser console for errors
- [ ] Verify new features work as expected

## Commands

### Run Local Tests
```bash
# Start Flask app locally
python app.py

# Visit http://localhost:5001 in browser
```

### Deploy to Production
```bash
# Make sure you're on main and up to date
git checkout main
git pull origin main

# Merge into deploy (triggers deployment)
git checkout deploy
git pull origin deploy
git merge main
git push origin deploy

# Monitor deployment at:
# https://github.com/savantlab/portfolio/actions
```

### Rollback (if needed)
```bash
git checkout deploy
git reset --hard <previous-commit-hash>
git push origin deploy --force
```

## Automated Checks

The Test Pipeline automatically runs when you push to `main`:

1. ✓ **Linting** - Checks for syntax errors
2. ✓ **Code Formatting** - Validates code style
3. ✓ **Import Validation** - Ensures Flask app imports
4. ✓ **File Structure** - Verifies required files exist
5. ✓ **Data Validation** - Checks PROJECTS and PUBLICATIONS structure
6. ✓ **Route Testing** - Tests all Flask routes
7. ✓ **Security Scan** - Checks for vulnerable dependencies

## Troubleshooting

### Tests Failing?
1. Check GitHub Actions logs for details
2. Fix issues locally
3. Push to main again
4. Wait for tests to pass

### Deployment Stuck?
1. Check GitHub Actions deployment logs
2. SSH into server to check status
3. Check gunicorn logs: `tail -f /flask/gunicorn.log`

### Site Not Updating?
1. Clear browser cache (Cmd+Shift+R)
2. Check deployment completed successfully
3. SSH to server and verify git pull happened
4. Restart gunicorn manually if needed

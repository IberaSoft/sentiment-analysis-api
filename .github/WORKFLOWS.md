# GitHub Workflows Documentation

This document explains the CI/CD workflows for the sentiment-analysis-api project.

## Workflows

### 1. Tests (`test.yml`)

**Trigger:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Steps:**
1. **Checkout code**
2. **Free up disk space** - Removes unused tools to prevent "No space left on device" errors
3. **Set up Python 3.11** - With pip caching enabled
4. **Install dependencies** - Installs requirements-dev.txt (includes all dev tools)
5. **Run linter** - Checks code quality with flake8, black, and isort
6. **Run tests** - Executes unit tests with coverage reporting
7. **Upload coverage** - Sends coverage report to Codecov

**Local Testing:**
```bash
# Install dependencies
pip install -r requirements-dev.txt

# Run linter
flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
black --check app/
isort --check app/

# Run tests
pytest tests/unit/ -v --cov=app --cov-report=xml
```

### 2. Deploy (`deploy.yml`)

**Trigger:**
- Push to `main` branch
- Push tags matching `v*` (e.g., v1.0.0)

**Steps:**
1. **Checkout code**
2. **Set up Docker Buildx** - For multi-platform builds
3. **Login to Docker Hub** - Uses secrets for authentication
4. **Build and push** - Builds Docker image and pushes to Docker Hub

**Tags Created:**
- `iberasoft/sentiment-api:latest` - Always points to the latest main build
- `iberasoft/sentiment-api:<commit-sha>` - Specific commit for rollback capability

## Required Secrets

For the workflows to function properly, configure these secrets in GitHub Settings → Secrets and variables → Actions:

### Docker Hub Secrets

1. **DOCKER_USERNAME**
   - Your Docker Hub username
   - Example: `iberasoft`

2. **DOCKER_PASSWORD**
   - Docker Hub access token (NOT your password)
   - How to create:
     1. Go to https://hub.docker.com/settings/security
     2. Click "New Access Token"
     3. Name: "GitHub Actions - sentiment-analysis-api"
     4. Permissions: Read, Write, Delete
     5. Copy the token and add it to GitHub secrets

### Codecov (Optional)

- **CODECOV_TOKEN** - For private repositories (public repos don't need this)

## Troubleshooting

### Test Workflow Issues

#### "Run linter" Step Fails

**Common Causes:**

1. **Black formatting issues**
   ```
   Error: Black formatting issues found
   ```
   **Solution:**
   ```bash
   black app/
   git add app/
   git commit -m "Fix: Apply black formatting"
   ```

2. **Import sorting issues**
   ```
   Error: Import sorting issues found
   ```
   **Solution:**
   ```bash
   isort app/
   git add app/
   git commit -m "Fix: Sort imports with isort"
   ```

3. **Flake8 errors**
   ```
   Error: Flake8 found issues
   ```
   **Solution:** Review the specific errors and fix them manually

#### "Install dependencies" Step Fails

**Cause:** Disk space issues or dependency conflicts

**Solution:**
- The workflow already frees up disk space
- If still failing, consider reducing dependencies or using a larger runner

#### "Run tests" Step Fails

**Cause:** Test failures or import errors

**Solution:**
```bash
# Run tests locally first
pytest tests/unit/ -v

# Fix any failing tests
# Then commit the fixes
```

### Deploy Workflow Issues

#### "Login to Docker Hub" Step Fails

**Common Causes:**

1. **Missing secrets**
   ```
   Error: Username and password required
   ```
   **Solution:** Add DOCKER_USERNAME and DOCKER_PASSWORD secrets in GitHub repo settings

2. **Invalid credentials**
   ```
   Error: unauthorized: authentication required
   ```
   **Solution:**
   - Verify DOCKER_USERNAME is correct
   - Regenerate DOCKER_PASSWORD token on Docker Hub
   - Update the secret in GitHub

3. **Token expired**
   ```
   Error: unauthorized: authentication required
   ```
   **Solution:** Generate a new Docker Hub access token and update the secret

#### "Build and push" Step Fails

**Common Causes:**

1. **Dockerfile errors**
   ```
   Error: failed to solve: process "/bin/sh -c ..." did not complete successfully
   ```
   **Solution:** Test Dockerfile locally:
   ```bash
   docker build -t sentiment-api:test .
   ```

2. **Push permission denied**
   ```
   Error: denied: requested access to the resource is denied
   ```
   **Solution:** Verify Docker Hub token has Write permissions

3. **Network issues**
   ```
   Error: failed to do request: ... dial tcp: i/o timeout
   ```
   **Solution:** Retry the workflow (temporary GitHub/Docker Hub connectivity issue)

## Workflow Improvements

### Conditional Execution

The deploy workflow now includes conditionals to ensure:
- Only runs on pushes to `main` or version tags
- Doesn't attempt deployment on pull requests
- Fails fast if Docker Hub login fails

### Caching

- **pip cache**: Speeds up Python dependency installation
- **Docker layer cache**: Reuses layers from previous builds

### Error Messages

Improved error messages help developers quickly identify and fix issues:
- Clear descriptions of what went wrong
- Suggestions for how to fix the problem
- Links to relevant documentation

## Manual Deployment

To manually deploy without GitHub Actions:

```bash
# Login to Docker Hub
docker login -u iberasoft

# Build image
docker build -t iberasoft/sentiment-api:latest .

# Push to Docker Hub
docker push iberasoft/sentiment-api:latest
```

## Monitoring Workflows

### View Workflow Runs

1. Go to your GitHub repository
2. Click "Actions" tab
3. Select the workflow you want to view
4. Click on a specific run to see details

### Enable Notifications

1. Go to repository Settings → Notifications
2. Configure email/Slack notifications for workflow failures

## Best Practices

1. **Test locally first** - Always run linting and tests locally before pushing
2. **Use feature branches** - Don't push directly to main
3. **Keep secrets secure** - Never commit secrets to the repository
4. **Monitor workflow runs** - Check for failures and fix them promptly
5. **Update dependencies regularly** - Keep actions and Python packages up to date

## Maintenance

### Updating Actions

Regularly update GitHub Actions to the latest versions:

```yaml
# Current versions
- uses: actions/checkout@v3           # Check for v4
- uses: actions/setup-python@v4       # Check for v5
- uses: docker/login-action@v2        # Check for v3
- uses: docker/build-push-action@v4   # Check for v5
```

### Updating Python Version

To update the Python version used in CI:

1. Update `.github/workflows/test.yml` line 26:
   ```yaml
   python-version: '3.12'  # Update as needed
   ```

2. Update `Dockerfile` line 1:
   ```dockerfile
   FROM python:3.12-slim
   ```

3. Test locally with the new version before committing

---

**Last Updated:** December 30, 2025
**Maintainer:** IberaSoft

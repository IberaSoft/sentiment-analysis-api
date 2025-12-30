# Docker Hub Setup Guide for GitHub Actions

## Issue
The deploy workflow is failing with:
```
ERROR: failed to fetch oauth token: 401 Unauthorized: access token has insufficient scopes
```

## Root Cause
The Docker Hub Personal Access Token (PAT) stored in GitHub Secrets doesn't have the required permissions to push images.

## Solution

### Step 1: Create a New Docker Hub Access Token

1. **Login to Docker Hub**
   - Go to https://hub.docker.com
   - Sign in with your credentials

2. **Navigate to Access Tokens**
   - Click your username (top right)
   - Select "Account Settings"
   - Click "Security" in the left sidebar
   - Click "Personal access tokens" or "New Access Token"

3. **Create New Token**
   - **Token Description**: `GitHub Actions - sentiment-analysis-api`
   - **Access Permissions**: Select **"Read, Write, Delete"** (IMPORTANT!)
   - Click "Generate"

4. **Copy the Token**
   - ⚠️ **IMPORTANT**: Copy the token NOW - you won't be able to see it again!
   - Save it temporarily in a secure location

### Step 2: Update GitHub Secret

1. **Go to Your Repository**
   - Navigate to: https://github.com/IberaSoft/sentiment-analysis-api

2. **Access Secrets**
   - Click "Settings" tab
   - In left sidebar, expand "Secrets and variables"
   - Click "Actions"

3. **Update DOCKER_PASSWORD Secret**
   - Find `DOCKER_PASSWORD` in the list
   - Click the pencil icon (Edit) or "Update"
   - Paste the NEW token you just created
   - Click "Update secret"

4. **Verify DOCKER_USERNAME Secret**
   - Ensure `DOCKER_USERNAME` exists and is set to: `iberasoft`
   - If not, create it with value: `iberasoft`

### Step 3: Verify Repository Exists on Docker Hub

1. **Check if repository exists**
   - Go to https://hub.docker.com/r/iberasoft/sentiment-api
   - If it doesn't exist, create it:

2. **Create Repository (if needed)**
   - Login to Docker Hub
   - Click "Repositories"
   - Click "Create Repository"
   - **Name**: `sentiment-api`
   - **Visibility**: Public (or Private if you prefer)
   - Click "Create"

### Step 4: Test the Fix

1. **Trigger the Workflow**
   - Option A: Push a new commit to main
   - Option B: Re-run the failed workflow from GitHub Actions UI
   - Option C: Push a new tag (e.g., `git tag v0.0.2 && git push origin v0.0.2`)

2. **Monitor the Build**
   - Go to: https://github.com/IberaSoft/sentiment-analysis-api/actions
   - Click on the running workflow
   - Watch the "Login to Docker Hub" and "Build and push" steps
   - Both should succeed with green checkmarks ✅

## Common Issues

### Issue: "Repository not found"
**Solution**: Create the repository on Docker Hub first (see Step 3)

### Issue: "unauthorized: authentication required"
**Cause**: Wrong username or token

**Solution**: 
- Double-check `DOCKER_USERNAME` is exactly `iberasoft` (lowercase)
- Regenerate the access token with correct permissions

### Issue: Token already used/expired
**Solution**: Delete the old token on Docker Hub and create a fresh one

### Issue: "denied: requested access to the resource is denied"
**Cause**: Token doesn't have Write permissions

**Solution**: Create a new token with "Read, Write, Delete" permissions

## Verifying Success

After the workflow completes successfully, verify:

1. **Check Docker Hub**
   - Go to https://hub.docker.com/r/iberasoft/sentiment-api/tags
   - You should see:
     - `latest` tag
     - A tag with the commit SHA (e.g., `2b070c4`)

2. **Pull the Image Locally (Optional)**
   ```bash
   docker pull iberasoft/sentiment-api:latest
   docker run -p 8000:8000 iberasoft/sentiment-api:latest
   ```

## Security Best Practices

1. **Use Access Tokens, Not Password**
   - ✅ Always use Personal Access Tokens
   - ❌ Never use your Docker Hub password in GitHub Secrets

2. **Minimal Permissions**
   - Only grant the permissions needed (Read, Write for CI/CD)
   - Delete permission is optional but recommended for cleanup

3. **Rotate Tokens Regularly**
   - Update tokens every 6-12 months
   - Immediately revoke tokens if compromised

4. **Token Description**
   - Use descriptive names to track token usage
   - Include the project name and purpose

## Summary Checklist

Before marking this as complete, ensure:

- [ ] New Docker Hub token created with Read, Write, Delete permissions
- [ ] `DOCKER_PASSWORD` secret updated in GitHub with new token
- [ ] `DOCKER_USERNAME` secret is set to `iberasoft`
- [ ] Docker Hub repository `iberasoft/sentiment-api` exists
- [ ] Workflow re-run and passes successfully
- [ ] Docker image visible on Docker Hub with correct tags

---

**Last Updated**: December 30, 2025
**Status**: Requires Action - Token needs to be regenerated

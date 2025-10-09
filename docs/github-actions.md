# GitHub Actions CI/CD Setup для NoteHub

Настройка GitHub Actions workflows для проекта NoteHub - автоматизация тестирования, линтинга и деплоя FastAPI приложения.

## Workflows Overview

### 1. CI Pipeline (`ci.yml`)

**Triggers:**
- Push to `main`, `master`, or `develop` branches
- Pull requests to these branches

**Jobs:**
- **test**: Runs unit tests with PostgreSQL service
- **docker-build**: Builds and tests Docker containers
- **docker-compose-test**: Tests full stack with docker-compose
- **security-scan**: Vulnerability scanning with Trivy
- **lint**: Code quality checks (Black, isort, flake8, mypy)

### 2. Deploy Pipeline (`deploy.yml`)

**Triggers:**
- Release published
- Manual workflow dispatch

**Jobs:**
- **build-and-push**: Builds and pushes Docker images to GitHub Container Registry
- **deploy-staging**: Deploys to staging environment
- **deploy-production**: Deploys to production environment

## Setup Instructions

### 1. Repository Settings

#### Secrets (if needed for deployment)
```
Settings → Secrets and variables → Actions
```

Add any required secrets for deployment:
- `DEPLOY_HOST`: Server hostname
- `DEPLOY_USER`: SSH username
- `DEPLOY_KEY`: SSH private key
- `DATABASE_URL`: Production database URL

#### Environments
```
Settings → Environments
```

Create environments:
- `staging`: For staging deployments
- `production`: For production deployments (with protection rules)

### 2. Branch Protection Rules

```
Settings → Branches → Add rule
```

Recommended settings for `main`/`master`:
- ✅ Require a pull request before merging
- ✅ Require status checks to pass before merging
  - ✅ test
  - ✅ docker-build
  - ✅ lint
- ✅ Require branches to be up to date before merging
- ✅ Restrict pushes that create files larger than 100MB

### 3. GitHub Container Registry

The workflows are configured to push Docker images to GitHub Container Registry (ghcr.io).

**Package visibility:**
```
Settings → Packages → notehub → Package settings → Change visibility
```

Set to Public if you want the images to be publicly accessible.

## Local Testing

### Prerequisites
```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Install Docker and Docker Compose
```

### Run Local CI Simulation

**Linux/Mac:**
```bash
chmod +x scripts/local-ci.sh
./scripts/local-ci.sh
```

**Windows PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\scripts\local-ci.ps1
```

### Manual Testing Steps

1. **Linting:**
```bash
cd backend
black --check app/ tests/
isort --check-only app/ tests/
flake8 app/ tests/
mypy app/ --ignore-missing-imports
```

2. **Unit Tests:**
```bash
cd backend
export PYTHONPATH=$PWD  # Linux/Mac
$env:PYTHONPATH = $PWD  # Windows PowerShell
python -m pytest tests/ -v --cov=app
```

3. **Docker Build:**
```bash
cd backend
docker build -t notehub-backend:test .
```

4. **Full Stack Test:**
```bash
cd backend
docker-compose up -d
# Wait for services...
curl http://localhost:8000/health
docker-compose down
```

## Workflow Configuration Details

### Test Matrix

The CI runs tests against:
- Python 3.13
- PostgreSQL 15
- Latest Ubuntu runner

### Docker Images

Built images are tagged with:
- Branch name (for branch pushes)
- PR number (for pull requests)
- Semantic version (for releases)
- Git SHA (always)

**Note**: All workflows use `docker compose` (without hyphen) which is the modern Docker Compose command available in GitHub Actions runners.

### Coverage Reports

Test coverage is:
- Displayed in terminal output
- Uploaded to Codecov (if configured)
- Available as XML report artifact

### Security Scanning

Trivy scanner checks for:
- Known vulnerabilities in dependencies
- Misconfigured Docker images
- Security best practices

## Customization

### Adding New Test Environments

To test against different Python versions:

```yaml
strategy:
  matrix:
    python-version: ["3.11", "3.12", "3.13"]
```

### Custom Deployment Steps

Replace the deployment steps in `deploy.yml` with your specific deployment commands:

```yaml
- name: Deploy to production
  run: |
    # Example for kubectl deployment
    kubectl set image deployment/notehub-backend app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
    kubectl rollout status deployment/notehub-backend
```

### Additional Checks

Add more quality checks to the lint job:

```yaml
- name: Run bandit security linter
  run: |
    pip install bandit
    bandit -r app/

- name: Check docstring coverage
  run: |
    pip install docstr-coverage
    docstr-coverage app/
```

## Troubleshooting

### Common Issues

1. **Tests failing in CI but passing locally:**
   - Check environment variables
   - Verify PostgreSQL service configuration
   - Check Python version differences

2. **Docker build fails:**
   - Verify Dockerfile syntax
   - Check if all dependencies are in requirements.txt
   - Ensure COPY paths are correct

3. **Linting failures:**
   - Run formatters locally: `black app/ tests/`
   - Sort imports: `isort app/ tests/`
   - Fix type hints for mypy

4. **Permission errors:**
   - Check if GITHUB_TOKEN has sufficient permissions
   - Verify repository settings allow Actions

### Debug Mode

Enable debug logging by adding to workflow:

```yaml
env:
  ACTIONS_STEP_DEBUG: true
```

### Manual Workflow Trigger

Test workflows manually:
```
Actions → Select workflow → Run workflow
```
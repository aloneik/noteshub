# Local CI test script for Windows PowerShell

Write-Host "🚀 Running local CI simulation..." -ForegroundColor Green

Set-Location backend

Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "🔍 Running linting checks..." -ForegroundColor Yellow
Write-Host "  - Black formatter check..." -ForegroundColor Cyan
black --check --diff app/ tests/

Write-Host "  - isort import sorting check..." -ForegroundColor Cyan
isort --check-only --diff app/ tests/

Write-Host "  - flake8 linter..." -ForegroundColor Cyan
flake8 app/ tests/

Write-Host "  - mypy type checker..." -ForegroundColor Cyan
mypy app/ --ignore-missing-imports

Write-Host "🧪 Running tests..." -ForegroundColor Yellow
$env:PYTHONPATH = $PWD
python -m pytest tests/ -v --cov=app --cov-report=term-missing

Write-Host "🐳 Testing Docker build..." -ForegroundColor Yellow
docker build -t notehub-backend:local-test .

Write-Host "✅ Local CI simulation completed!" -ForegroundColor Green
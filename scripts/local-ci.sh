#!/bin/bash
# Local CI test script

echo "🚀 Running local CI simulation..."

cd backend

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🔍 Running linting checks..."
echo "  - Black formatter check..."
black --check --diff app/ tests/

echo "  - isort import sorting check..."
isort --check-only --diff app/ tests/

echo "  - flake8 linter..."
flake8 app/ tests/

echo "  - mypy type checker..."
mypy app/ --ignore-missing-imports

echo "🧪 Running tests..."
export PYTHONPATH=$PWD
python -m pytest tests/ -v --cov=app --cov-report=term-missing

echo "🐳 Testing Docker build..."
docker build -t notehub-backend:local-test .

echo "✅ Local CI simulation completed!"
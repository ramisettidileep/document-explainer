#!/usr/bin/env bash
set -e

echo "=== Document Explainer Agent: Offline Verification Suite ==="

echo "1. Checking Python Syntax..."
python3 -m py_compile $(find backend tests -name "*.py")
echo "✓ Python syntax valid."

echo "2. Running Backend Unit Tests..."
PYTHONPATH=. python3 -m unittest discover -s tests/backend -p "test_*.py"
echo "✓ Backend tests passed."

echo "3. Testing Frontend Production Build..."
cd frontend
npm run build
cd ..
echo "✓ Frontend build succeeded."

echo "=== All Offline Checks Passed! ==="
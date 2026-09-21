#!/usr/bin/env bash
export ENVIRONMENT=local
export OLLAMA_BASE_URL=${OLLAMA_BASE_URL:-http://127.0.0.1:11434}
export OLLAMA_MODEL=${OLLAMA_MODEL:-llama3.2}

echo "Starting Document Explainer SAM Backend on port 3000..."
sam local start-api --port 3000 --env-vars backend/env.json
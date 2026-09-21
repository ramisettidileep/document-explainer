#!/usr/bin/env bash
set -e

API_BASE=${API_BASE_URL:-http://localhost:3000}
echo "Testing API at: $API_BASE"

RESPONSE=$(curl -s -X POST "$API_BASE/documents" \
  -H "Content-Type: application/json" \
  -H "X-User-Id: demo-user" \
  -d '{"text": "Agreement between Party A and B requires notice of 30 days for termination.", "file_name": "test.txt"}')

echo "Response: $RESPONSE"
DOC_ID=$(echo "$RESPONSE" | grep -o '"id": "[^"]*' | cut -d'"' -f4)

if [ -n "$DOC_ID" ]; then
  curl -s -X GET "$API_BASE/documents/$DOC_ID" -H "X-User-Id: demo-user"
  curl -s -X POST "$API_BASE/documents/$DOC_ID/chat" \
    -H "Content-Type: application/json" \
    -H "X-User-Id: demo-user" \
    -d '{"question": "termination"}'
fi
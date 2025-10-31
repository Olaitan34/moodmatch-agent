#!/bin/bash

# Test the health endpoint
echo "Testing health endpoint..."
curl http://localhost:8000/health
echo -e "\n"

# Test the A2A endpoint
echo "Testing A2A endpoint with mood request..."
curl -X POST http://localhost:8000/a2a/moodmatch \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "test-123",
    "method": "message/send",
    "params": {
      "messages": [
        {
          "role": "user",
          "parts": [
            {
              "type": "text",
              "text": "I am feeling stressed and overwhelmed with work"
            }
          ]
        }
      ]
    }
  }'
echo -e "\n"

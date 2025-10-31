#!/bin/bash

# Test script for MoodMatch A2A Agent
# Sends a properly formatted A2A protocol request

echo "🧪 Testing MoodMatch A2A Agent..."
echo ""

# Test 1: Health Check
echo "1️⃣ Testing Health Endpoint..."
curl -s http://localhost:8000/health | python -m json.tool
echo ""
echo ""

# Test 2: Simple mood request
echo "2️⃣ Testing A2A Endpoint with stressed mood..."
curl -s -X POST http://localhost:8000/a2a/moodmatch \
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
              "text": "I am feeling stressed and overwhelmed. I need something to help me relax."
            }
          ]
        }
      ]
    }
  }' | python -m json.tool

echo ""
echo "✅ Test complete!"

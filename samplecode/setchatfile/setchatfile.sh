#!/bin/bash

# Set variables
GOVBOTIC_API_BASE_URL="http://localhost:8000"  # Replace with the actual base URL
ENDPOINT="/setfiledrawer/"
URL="${GOVBOTIC_API_BASE_URL}${ENDPOINT}"
BEARER_TOKEN="your_bearer_token_here"  # Replace with your actual bearer token

# JSON payload
REQUEST_PAYLOAD='{
  "requestType": "setchatfile",
  "persona": "AI Assistant",
  "uid": "user123",
  "message": "/CHAINOFTHOUGHT/2201.11903",
  "document": null,
  "context": "User asks for help.",
  "maxTokens": 150,
  "temperature": 0.5,
  "sessionId": "session456",
  "language": "en"
}'

# Curl command to send POST request
curl -X POST "$URL" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $BEARER_TOKEN" \
     -d "$REQUEST_PAYLOAD"

# Add additional commands or logic to handle the response as needed


#!/bin/bash
# Bash script to send a POST request to the FastAPI application
curl -X 'POST' \
  'http://127.0.0.1:8000/message/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer ${GOVBOTIC_API_TOKEN}' \
  -d '{
  "persona": "examplePersona",
  "uid": "exampleUID",
  "message": "Health Benefits of Lemons",
  "document": "LemonPeel/LemmonPeels",
  "context": "What is the Purpose of this manual?",
  "maxTokens": 100,
  "temperature": 0.5,
  "topP": 0.9,
  "stopSequences": ["\n"],
  "sessionId": "exampleUID",
  "language": "en-US",
  "requestType": "query"
}'


#!/bin/bash

# Define variables
GOVBOTIC_API_BASE_URL=http://127.0.0.1:8000
GOVBOTIC_API_TOKEN="FIFTOKENFORMAT"
ENDPOINT="/listfiledrawers/"

# JSON payload
REQUEST_DATA='{"requestType": "listfiles", "dataOperands": "YourDataOperands", "fileNames": ["file1.txt", "file2.txt"]}'

# cURL command
while true
do
echo ""
echo ""
curl -X POST "${GOVBOTIC_API_BASE_URL}${ENDPOINT}" \
     -H "Authorization: Bearer ${GOVBOTIC_API_TOKEN}" \
     -H "Content-Type: application/json" \
     -d "${REQUEST_DATA}"
done


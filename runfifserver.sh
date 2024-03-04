#!/bin/bash

# Set environment variables
export GOVBOTIC_INGESTION_STORAGE="/Users/randolphhill/govbotics/deepinfra/Pansolusi/fifserver/ingestion/DOCUMENTS"
#export GOVBOTIC_INGESTION_STORAGE=""
export GOVBOTIC_FILE_SANDBOX="/Users/randolphhill/govbotics/deepinfra/Pansolusi/fifserver/ingestion/sandbox"
export GOVBOTIC_API_BASE_URL="http://127.0.0.1:8000"
export GOVBOTIC_API_TOKEN="FIFTOKENFORMAT"
export GOVBOTIC_ADMIN_SERVER="http://127.0.0.1:8050"
export GOVBOTIC_LLM_DEEPINFRA="True"

# Check each variable and print an error if not set
if [ -z "$GOVBOTIC_INGESTION_STORAGE" ]; then
    echo "Error: GOVBOTIC_INGESTION_STORAGE is not set."
fi

if [ -z "$GOVBOTIC_FILE_SANDBOX" ]; then
    echo "Error: GOVBOTIC_FILE_SANDBOX is not set."
fi

if [ -z "$GOVBOTIC_API_BASE_URL" ]; then
    echo "Error: GOVBOTIC_API_BASE_URL is not set."
fi

if [ -z "$GOVBOTIC_API_TOKEN" ]; then
    echo "Error: GOVBOTIC_API_TOKEN is not set."
fi

if [ -z "$GOVBOTIC_ADMIN_SERVER" ]; then
    echo "Error: GOVBOTIC_ADMIN_SERVER is not set."
fi

if [ -z "$GOVBOTIC_LLM_DEEPINFRA" ]; then
    echo "Error: GOVBOTIC_LLM_DEEPINFRA is not set."
fi

[ -d ".venv" ] || { echo "Error: .venv directory does not exist."; exit 1; }
source .venv/bin/activate
./backend/runserver.sh>/tmp/fiflog.log&
exit
./ingest/runingestserver.sh>>/tmp/fiflog.log&
exit
sleep 2
osascript -e 'tell app "Terminal" to do script "tail -f /tmp/fiflog.log"'



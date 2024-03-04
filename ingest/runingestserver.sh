#!/bin/bash
# Check each variable and print an error if not set


if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY not set"
    echo "Contact your administrator for a Open AI Key"
    exit
fi
if [ -z "$DEEPINFRA_API_TOKEN" ]; then
    echo "Error:DEEPINFRA_API_TOKEN not set."
    echo "Contact your Administrtor for an DeepInfra Key"
    exit
fi
if [ -z "$GOVBOTIC_INGESTION_STORAGE" ]; then
    echo "Error: GOVBOTIC_INGESTION_STORAGE is not set."
    exit
fi

if [ -z "$GOVBOTIC_FILE_SANDBOX" ]; then
    echo "Error: GOVBOTIC_FILE_SANDBOX is not set."
    exit
fi

if [ -z "$GOVBOTIC_API_BASE_URL" ]; then
    echo "Error: GOVBOTIC_API_BASE_URL is not set."
    exit
fi

if [ -z "$GOVBOTIC_API_TOKEN" ]; then
    echo "Error: GOVBOTIC_API_TOKEN is not set."
    exit
fi

if [ -z "$GOVBOTIC_ADMIN_SERVER" ]; then
    echo "Error: GOVBOTIC_ADMIN_SERVER is not set."
    exit
fi

if [ -z "$GOVBOTIC_LLM_DEEPINFRA" ]; then
    echo "Error: GOVBOTIC_LLM_DEEPINFRA is not set."
    exit
fi
if [ -d "$GOVBOTIC_INGESTION_STORAGE" ]; then
    echo "Directory path '${GOVBOTIC_INGESTION_STORAGE}' validated."
else
    echo "Error: Directory path '${GOVBOTIC_INGESTION_STORAGE}' does not exist."
    echo "Define a directory to store documents."
    exit
fi

if [ -d "$GOVBOTIC_FILE_SANDBOX" ]; then
    echo "Directory path '${GOVBOTIC_FILE_SANDBOX}' validated."
else
    echo "Error: Directory path '${GOVBOTIC_FILE_SANDBOX}' does not exist."
    echo "Need to designate a temp area for downloaded files."
    exit 1 # Indicates an error condition
fi

if [ -d "$GOVBOTIC_FILE_SANDBOX/bottomDrawer" ]; then
    echo "Directory path '${GOVBOTIC_FILE_SANDBOX}/bottomDrawer' validated."
else
    echo "Creating Bottom drawer in '${GOVBOTIC_FILE_SANDBOX}'"
    mkdir -p "$GOVBOTIC_FILE_SANDBOX/bottomDrawer" # This command actually creates the directory
fi

# Start the FastAPI application with Uvicorn with hot reload enabled
source ../.venv/bin/activate
# Start the FastAPI application with Uvicorn with hot reload enabled
uvicorn main:app --reload --host 0.0.0.0 --port 8050


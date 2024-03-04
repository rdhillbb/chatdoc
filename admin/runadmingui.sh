#!/bin/bash
if [ -f "../.venv/bin/activate" ]; then
    echo "Virtual environment activation script validated."
else
    echo "Error: Virtual Environment not created"
    echo "Exiting"
    exit
fi
# Start the FastAPI application with Uvicorn with hot reload enabled
curl -s http://0.0.0.0:8050 > /dev/null
if [ $? -eq 0 ]; then
    echo "Ingestion Service is running on http://0.0.0.0:8050"
else
    echo "ISSUE FOUND"
    echo "Ingestion Service not running is not running on http://0.0.0.0:8050"
    echo "Start the ingestion server in ../ingest/runingestserver.sh"
    echo ""
    exit
fi
source ../.venv/bin/activate
streamlit run app.py


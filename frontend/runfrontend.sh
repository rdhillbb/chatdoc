#!/bin/bash
if [ -f "../.venv/bin/activate" ]; then
    echo "Virtual environment activation script validated."
else
    echo "Error: Virtual Environment not created"
    echo "Exiting"
    exit
fi
# Start the FastAPI application with Uvicorn with hot reload enabled
curl -s http://0.0.0.0:8000 > /dev/null
if [ $? -eq 0 ]; then
    echo "Backend Chat service is running on http://0.0.0.0:8000"
else
    echo "ISSUE FOUND"
    echo "Backend Chat Service not running is not running on http://0.0.0.0:8000"
    echo "Start the ingestion server in ../backend/runserver.sh.sh"
    echo ""
    exit
fi
# Start the FastAPI application with Uvicorn with hot reload enabled
source ../.venv/bin/activate
# Start the FastAPI application with Uvicorn with hot reload enabled
streamlit run newgui.py

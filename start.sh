#!/bin/bash

echo "Starting Drone Geo-Localization Web Server..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from your package manager"
    exit 1
fi

# Check if dependencies are installed
python3 -c "import gradio" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
fi

echo
echo "========================================"
echo "  Drone Geo-Localization Web Server"
echo "========================================"
echo
echo "Starting server..."
echo "Access at: http://localhost:7860"
echo "Press Ctrl+C to stop"
echo

python3 app.py

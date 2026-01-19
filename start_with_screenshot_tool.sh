#!/bin/bash

# Start the Flask screenshot tool in the background on port 5001
echo "🖼️  Starting Screenshot Selection Tool..."
python screenshot_tool.py &
FLASK_PID=$!

# Give Flask a moment to start
sleep 2

# Start the main Gradio app
echo "🚀 Starting Main Application..."
python app.py

# Clean up Flask process when app exits
kill $FLASK_PID 2>/dev/null || true

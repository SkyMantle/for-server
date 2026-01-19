#!/bin/bash

# Start both the Flask screenshot tool and the main Gradio app
# This allows users to use the standalone screenshot selector if needed

echo "🚀 Starting Drone Geo-Localization App with Screenshot Tool"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Main App:"
echo "   http://localhost:7860"
echo ""
echo "🖱️  Screenshot Selector (standalone):"
echo "   http://localhost:5001"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

source .venv/bin/activate

# Start screenshot tool in background
python screenshot_tool.py &
SCREENSHOT_PID=$!

# Start main app (foreground so user can see logs)
python -u -O app.py

# Kill screenshot tool if main app exits
kill $SCREENSHOT_PID 2>/dev/null

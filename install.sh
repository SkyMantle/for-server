#!/bin/bash

echo "=========================================="
echo "  Drone Geo-Localization Installer"
echo "=========================================="
echo

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
fi

echo "Detected OS: $OS"
echo

# Check Python
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    echo
    if [ "$OS" == "mac" ]; then
        echo "Install with: brew install python3"
    elif [ "$OS" == "linux" ]; then
        echo "Install with: sudo apt install python3 python3-pip"
    fi
    exit 1
else
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "✅ Python $PYTHON_VERSION found"
fi

# Install dependencies
echo
echo "Installing Python dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo
    echo "✅ Installation complete!"
    echo
    echo "To start the server:"
    echo "  ./start.sh"
    echo
    echo "Or manually:"
    echo "  python3 app.py"
    echo
else
    echo
    echo "❌ Installation failed"
    echo "Please check the error messages above"
    exit 1
fi

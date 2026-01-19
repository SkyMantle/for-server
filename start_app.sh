#!/bin/bash
# Startup script for Drone Localization App - Optimized for Fast Startup

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the app directory
cd "$DIR"

# Activate virtual environment and run the app with optimizations
source .venv/bin/activate

# Use Python's -u flag for unbuffered output and startup optimizations
python -u -O app.py

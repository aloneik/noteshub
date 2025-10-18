#!/bin/bash
# Run NoteHub Desktop in DEBUG mode

echo "Starting NoteHub Desktop in DEBUG mode..."
echo

# Set debug mode
export NOTEHUB_DEBUG=1

# Activate virtual environment
source .venv/bin/activate

# Run application
python src/main.py

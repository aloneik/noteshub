#!/bin/bash
# Development script for Linux/macOS

echo "Starting NoteHub Desktop..."
echo ""
echo "Make sure backend is running:"
echo "  cd ../backend"
echo "  docker compose up -d"
echo ""

python3 src/main.py

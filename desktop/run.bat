@echo off
REM Development script for Windows

echo Starting NoteHub Desktop...
echo.
echo Make sure backend is running:
echo   cd ..\backend
echo   docker compose up -d
echo.

python src\main.py

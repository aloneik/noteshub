@echo off
REM Run NoteHub Desktop in DEBUG mode

echo Starting NoteHub Desktop in DEBUG mode...
echo.

REM Set debug mode
set NOTEHUB_DEBUG=1

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run application
python src\main.py

pause

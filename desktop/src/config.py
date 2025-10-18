"""Configuration for NoteHub Desktop Application."""

import os
import logging
from pathlib import Path

# Application Info
APP_NAME = "NoteHub"
APP_VERSION = "1.0.0"
APP_AUTHOR = "NoteHub"
APP_ORG = "NoteHub"

# Debug Mode
DEBUG = os.getenv("NOTEHUB_DEBUG", "0") == "1"

# Default Backend URL
DEFAULT_BACKEND_URL = os.getenv("NOTEHUB_BACKEND_URL", "http://localhost:8000")

# Paths
APP_DIR = Path(__file__).parent.parent
RESOURCES_DIR = APP_DIR / "resources"
ICONS_DIR = RESOURCES_DIR / "icons"
LOGS_DIR = APP_DIR / "logs"

# Logging Configuration
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# API Endpoints
API_ENDPOINTS = {
    "register": "/auth/register",
    "login": "/auth/login",
    "users_me": "/users/me",
    "notes": "/notes",
    "note_detail": "/notes/{note_id}",
    "plans": "/notes/{note_id}/plans",
    "plan_detail": "/notes/{note_id}/plans/{plan_id}",
}

# UI Settings
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600
WINDOW_DEFAULT_WIDTH = 1200
WINDOW_DEFAULT_HEIGHT = 800

# Theme
DARK_THEME = """
QMainWindow {
    background-color: #1e1e1e;
}
QWidget {
    background-color: #2d2d2d;
    color: #cccccc;
}
QPushButton {
    background-color: #0e639c;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #1177bb;
}
QPushButton:pressed {
    background-color: #0d5a8f;
}
QPushButton:disabled {
    background-color: #3d3d3d;
    color: #888888;
}
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #3c3c3c;
    color: #cccccc;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 6px;
}
QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #0e639c;
}
QListWidget {
    background-color: #252526;
    color: #cccccc;
    border: 1px solid #3c3c3c;
    border-radius: 4px;
}
QListWidget::item {
    padding: 8px;
    border-bottom: 1px solid #3c3c3c;
}
QListWidget::item:selected {
    background-color: #094771;
}
QListWidget::item:hover {
    background-color: #2a2d2e;
}
QLabel {
    color: #cccccc;
}
QMenuBar {
    background-color: #2d2d2d;
    color: #cccccc;
}
QMenuBar::item:selected {
    background-color: #094771;
}
QMenu {
    background-color: #2d2d2d;
    color: #cccccc;
    border: 1px solid #3c3c3c;
}
QMenu::item:selected {
    background-color: #094771;
}
QStatusBar {
    background-color: #007acc;
    color: white;
}
QScrollBar:vertical {
    background-color: #2d2d2d;
    width: 12px;
}
QScrollBar::handle:vertical {
    background-color: #555555;
    border-radius: 6px;
}
QScrollBar::handle:vertical:hover {
    background-color: #666666;
}
"""

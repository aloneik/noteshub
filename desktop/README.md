# NoteHub Desktop

Desktop application for NoteHub notes and daily plans management.

## Tech Stack

- **Framework**: PySide6 (Qt for Python)
- **Language**: Python 3.11+
- **Build Tool**: Nuitka (compile to native executable)
- **API Client**: requests
- **Platforms**: Windows, Linux, macOS

## Features

- 🔐 Login/Register with JWT authentication
- 📝 Notes management (create, edit, delete)
- 📅 Daily plans for each note
- ⚙️ Settings (backend URL, theme)
- 🪟 Native system integration
- 💾 Single executable file (~20 MB)

## Quick Start

### Development

1. **Install Dependencies**:
```bash
cd desktop
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

2. **Run Application**:
```bash
# Normal mode
python src/main.py

# Debug mode (with detailed logging)
run_debug.bat          # Windows
./run_debug.sh         # Linux/macOS
```

3. **Configure Backend URL**:
   - Default: `http://localhost:8000`
   - Can be changed in Settings

### Debug Mode

Enable debug mode to see detailed logs:

**Windows**:
```powershell
$env:NOTEHUB_DEBUG="1"
python src/main.py
```

**Linux/macOS**:
```bash
export NOTEHUB_DEBUG=1
python src/main.py
```

Debug logs include:
- API requests/responses
- Authentication flow
- UI events
- Error stack traces

Logs are saved to: `logs/notehub_YYYYMMDD_HHMMSS.log`

### Building Executable

#### Windows
```bash
python build.py windows
# Result: dist/NoteHub.exe (~20 MB)
```

#### Linux
```bash
python build.py linux
# Result: dist/NoteHub (~20 MB)
```

#### macOS
```bash
python build.py macos
# Result: dist/NoteHub.app (~25 MB)
```

## Project Structure

```
desktop/
├── src/
│   ├── main.py              # Application entry point
│   ├── config.py            # Application configuration
│   ├── ui/
│   │   ├── login_window.py  # Login/Register window
│   │   ├── main_window.py   # Main application window
│   │   ├── note_editor.py   # Note editing widget
│   │   └── settings.py      # Settings dialog
│   ├── api/
│   │   └── client.py        # FastAPI backend client
│   └── models/
│       ├── user.py          # User model
│       ├── note.py          # Note model
│       └── plan.py          # Plan model
├── resources/
│   └── icons/               # Application icons
├── requirements.txt         # Python dependencies
├── build.py                 # Nuitka build script
└── README.md               # This file
```

## Backend Requirements

The desktop app requires NoteHub backend running:

```bash
cd ../backend
docker compose up -d
```

Backend should be accessible at configured URL (default: `http://localhost:8000`).

## Development Tips

### Hot Reload
Just save changes and restart `python src/main.py` - PySide6 doesn't have hot reload like web frameworks.

### Qt Designer
For visual UI design:
```bash
pyside6-designer
```

### Debugging
Use Qt's built-in debugging:
```python
from PySide6.QtCore import qDebug
qDebug("Debug message")
```

### Styling
Qt supports CSS-like styling:
```python
widget.setStyleSheet("background-color: #1e1e1e; color: white;")
```

## Distribution

### Windows
- Single `.exe` file (portable)
- Optional: Create installer with Inno Setup

### Linux
- Binary file or AppImage
- Optional: Create `.deb`/`.rpm` package

### macOS
- `.app` bundle
- Optional: Sign and notarize for distribution

## License

Same as main NoteHub project.

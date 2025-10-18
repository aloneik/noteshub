# Debug Mode & Logging

NoteHub Desktop has comprehensive logging support for debugging and troubleshooting.

## Quick Start

### Enable Debug Mode

**Windows (PowerShell)**:
```powershell
$env:NOTEHUB_DEBUG="1"
python src\main.py
```

**Windows (Batch)**:
```batch
run_debug.bat
```

**Linux/macOS**:
```bash
export NOTEHUB_DEBUG=1
python src/main.py
# or
./run_debug.sh
```

## Log Levels

### Production Mode (default)
- **Level**: INFO
- **Output**: File only
- **Location**: `logs/notehub_YYYYMMDD_HHMMSS.log`

Logs include:
- Application startup/shutdown
- User authentication
- API requests (method + URL + status code)
- Errors with basic information

### Debug Mode (`NOTEHUB_DEBUG=1`)
- **Level**: DEBUG
- **Output**: Console + File
- **Location**: `logs/notehub_YYYYMMDD_HHMMSS.log`

Additional logs include:
- Qt application initialization
- UI events
- Detailed API request/response
- Full error stack traces
- Internal state changes

## Log Format

```
YYYY-MM-DD HH:MM:SS - module.name - LEVEL - Message
```

Example:
```
2025-10-18 19:24:54 - api.client - INFO - API Client initialized with base URL: http://localhost:8000
2025-10-18 19:24:58 - api.client - DEBUG - Request successful: POST http://localhost:8000/auth/login -> 200
2025-10-18 19:24:59 - __main__ - INFO - User loaded: testuser (ID: 1)
```

## What Gets Logged

### Application Lifecycle
- ✅ Application start
- ✅ Qt initialization
- ✅ Theme application
- ✅ Settings loading
- ✅ API client setup
- ✅ Window creation
- ✅ Application exit

### Authentication
- ✅ Registration attempts
- ✅ Login attempts
- ✅ Token creation
- ✅ User info loading

### API Operations
- ✅ All HTTP requests (method, URL, status)
- ✅ Request failures with error details
- ✅ Full stack traces for exceptions (DEBUG mode)

### UI Events (DEBUG mode)
- ✅ Window show/hide
- ✅ Dialog open/close
- ✅ User actions

## Log Management

### Location
All logs are stored in: `desktop/logs/`

### Filename Format
`notehub_YYYYMMDD_HHMMSS.log`

Example: `notehub_20251018_192454.log`

### Cleanup
Logs are not automatically deleted. To clean up old logs:

**Windows**:
```powershell
Remove-Item logs\*.log -Force
```

**Linux/macOS**:
```bash
rm -f logs/*.log
```

## Viewing Logs

### Real-time (Console)
Debug mode shows logs in console in real-time.

### File Viewing

**Windows**:
```powershell
# View last log
Get-Content (Get-ChildItem logs\*.log | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName

# View last 50 lines
Get-Content (Get-ChildItem logs\*.log | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName -Tail 50

# Follow log (real-time)
Get-Content (Get-ChildItem logs\*.log | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName -Wait
```

**Linux/macOS**:
```bash
# View last log
cat logs/$(ls -t logs/ | head -1)

# View last 50 lines
tail -50 logs/$(ls -t logs/ | head -1)

# Follow log (real-time)
tail -f logs/$(ls -t logs/ | head -1)
```

## Troubleshooting

### Problem: No logs generated
**Solution**: Check that `logs/` directory exists. It should be created automatically.

### Problem: Too many logs
**Solution**: Logs accumulate over time. Clean them periodically (see Cleanup section).

### Problem: Can't find log file
**Solution**: Check console output at startup - it shows the log file path:
```
INFO [root] Log file: C:\...\desktop\logs\notehub_20251018_192454.log
```

### Problem: Need more details
**Solution**: Enable DEBUG mode for verbose logging.

## Privacy & Security

⚠️ **Important**: Debug logs contain sensitive information:
- Authentication tokens (first 20 characters shown)
- API responses (may include user data)
- Error stack traces

**Never share debug logs publicly without sanitizing them first!**

## Production Builds

When building with Nuitka, logs are still generated but:
- Default level is INFO (not DEBUG)
- Console output is hidden (Windows)
- Logs go to `logs/` directory next to executable

To enable debug mode in production build:
```bash
# Set environment variable before running executable
set NOTEHUB_DEBUG=1
NoteHub.exe
```

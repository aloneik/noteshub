# Desktop Application Testing Guide

## Prerequisites

1. **Backend must be running**:
   ```bash
   cd ../backend
   docker compose up -d
   ```

2. **Desktop dependencies installed**:
   ```bash
   cd desktop
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # Windows
   pip install -r requirements.txt
   ```

## Testing Options

### Option 1: Automated API Test

Quick test to verify API client works:

```bash
python test_api.py
```

This will:
- ✅ Check backend connection
- ✅ Test user registration
- ✅ Test login
- ✅ Test notes CRUD operations

**Expected output:**
```
🚀 NoteHub Desktop - API Client Test

🔌 Testing connection to http://localhost:8000
✅ Backend is reachable!
   Swagger docs available at: http://localhost:8000/docs

📝 Testing registration...
✅ Registration successful!
   Username: testuser_1234
   User ID: 1

🔐 Testing login...
✅ Login successful!
   Token: eyJhbGciOiJIUzI1NiIs...

📝 Testing notes...
✅ Created note: Test Note (ID: 1)
✅ Retrieved 1 note(s)
✅ Updated note: Updated Test Note
✅ Deleted note

✅ All tests completed!
```

### Option 2: Manual UI Testing

Run the desktop application:

```bash
python src/main.py
# or
.\run.bat  # Windows
./run.sh   # Linux/macOS
```

**Test scenarios:**

1. **Registration Flow**
   - Click "Register" tab
   - Enter username: `testuser1`
   - Enter password: `password123`
   - Confirm password: `password123`
   - Click "Register" button
   - ✅ Should show success message and switch to Login tab

2. **Login Flow**
   - Username: `testuser1`
   - Password: `password123`
   - Click "Login" button
   - ✅ Should close login window and open main window

3. **Notes Management**
   - Click "+ New Note" button
   - ✅ Note created with title "Untitled Note"
   - Change title to "My First Note"
   - Add content: "This is my first note"
   - Click "💾 Save" button
   - ✅ Should see "Note saved" in status bar

4. **Plans Management**
   - Select a note from list
   - Click "+ Add Plan" button
   - Set date to today
   - Enter content: "Complete desktop app testing"
   - Click "OK"
   - ✅ Plan should appear in plans list
   - Click checkbox to mark as completed
   - ✅ Plan text should have strikethrough

5. **Delete Operations**
   - Select a plan and click "🗑️" button
   - ✅ Plan removed from list
   - Select a note and click "🗑️ Delete" button
   - Confirm deletion
   - ✅ Note removed from list, editor cleared

## UI Verification Checklist

- [ ] Login window appears on startup
- [ ] Login window has dark theme styling
- [ ] Registration validates password length (min 6 chars)
- [ ] Registration validates password match
- [ ] Login shows error on invalid credentials
- [ ] Main window opens after successful login
- [ ] Username shown in window title
- [ ] Notes list on left sidebar
- [ ] Note editor on right panel
- [ ] Can create new notes
- [ ] Can edit note title and content
- [ ] Can save notes
- [ ] Can delete notes (with confirmation)
- [ ] Plans section shows below note content
- [ ] Can add plans with date picker
- [ ] Can mark plans as completed (checkbox)
- [ ] Can delete plans
- [ ] Status bar shows feedback messages
- [ ] Refresh button reloads notes from server

## Error Testing

1. **Backend Not Running**
   - Stop backend: `cd ../backend && docker compose down`
   - Try to login in desktop app
   - ✅ Should show connection error message

2. **Invalid Credentials**
   - Enter wrong password
   - ✅ Should show "Login Failed" error

3. **Empty Fields**
   - Try to save note with empty title
   - ✅ Should show validation error

4. **Network Issues**
   - Disconnect internet (if using Cloudflare tunnel)
   - Try to load notes
   - ✅ Should show error message

## Performance Testing

- [ ] App starts in < 3 seconds
- [ ] Login response < 1 second
- [ ] Notes list loads in < 2 seconds
- [ ] Note selection opens instantly
- [ ] No UI freezing during operations

## Cross-Platform Testing (if applicable)

### Windows
- [ ] .exe builds successfully
- [ ] .exe runs without dependencies
- [ ] Dark theme renders correctly
- [ ] Emoji in buttons display properly

### Linux
- [ ] Binary builds successfully
- [ ] App runs on Ubuntu/Debian
- [ ] GTK/Qt integration works

### macOS
- [ ] .app builds successfully
- [ ] App runs on macOS 11+
- [ ] Retina display renders correctly

## Troubleshooting

### Import Errors
```bash
# Make sure you're in the virtual environment
.\.venv\Scripts\Activate.ps1
# Verify PySide6 is installed
pip list | grep PySide6
```

### API Connection Errors
```bash
# Check backend is running
curl http://localhost:8000/docs
# Check logs
cd ../backend
docker compose logs backend
```

### Qt Platform Plugin Errors
```bash
# Windows: Usually means Qt DLLs are missing
pip install --force-reinstall PySide6
```

## Building Executable

Once testing is complete, build standalone executable:

```bash
python build.py windows  # or linux, macos
```

Binary will be in `dist/` folder (~20 MB).

Test the built executable on a clean system without Python installed.

# Manual Testing Guide

## Overview
This project uses manual testing. Follow these test scenarios to verify functionality before deployment.

## Prerequisites
- Backend running on `http://localhost:8000`
- Frontend running on `http://localhost:5173`
- Or use Cloudflare tunnels for internet access

## Test Scenarios

### 1. Authentication Flow

#### Registration
1. Open frontend in browser
2. Click "Register" or go to `/register`
3. Enter username: `testuser1` and password: `Test123456!`
4. Click "Register"
5. ✅ **Expected**: Redirect to login page with success message

#### Login
1. Go to `/login`
2. Enter credentials from registration
3. Click "Login"
4. ✅ **Expected**: Redirect to dashboard, see welcome message

#### Logout
1. Click "Logout" button in header
2. ✅ **Expected**: Redirect to login, token cleared from localStorage

### 2. Notes CRUD Operations

#### Create Note
1. Login first
2. Click "New Note" or "+" button
3. Enter title: `My First Note`
4. Enter content: `This is test content`
5. Click "Save"
6. ✅ **Expected**: Note appears in notes list

#### Read Notes
1. Check notes list on dashboard
2. Click on a note to view details
3. ✅ **Expected**: Note opens with full content and plans section

#### Update Note
1. Open a note
2. Click "Edit" button
3. Change title to: `Updated Note Title`
4. Change content
5. Click "Save"
6. ✅ **Expected**: Note updated, changes visible immediately

#### Delete Note
1. Open a note
2. Click "Delete" button
3. Confirm deletion
4. ✅ **Expected**: Note removed from list, redirect to dashboard

### 3. Plans CRUD Operations

#### Create Plan
1. Open any note
2. Find "Plans" section
3. Click "Add Plan"
4. Enter plan details:
   - Date: `2025-10-20`
   - Content: `Complete testing documentation`
5. Click "Save"
6. ✅ **Expected**: Plan appears in note's plans list

#### Update Plan
1. Click "Edit" on a plan
2. Change content to: `Updated plan content`
3. Mark as completed (if checkbox available)
4. Click "Save"
5. ✅ **Expected**: Plan updated with new content

#### Delete Plan
1. Click "Delete" on a plan
2. Confirm deletion
3. ✅ **Expected**: Plan removed from list

### 4. Data Persistence

#### Browser Refresh
1. Create a note with plans
2. Refresh the page (F5)
3. ✅ **Expected**: All data still present, still logged in

#### Logout/Login
1. Create note and plan
2. Logout
3. Login with same credentials
4. ✅ **Expected**: All notes and plans still visible

### 5. User Isolation

#### Different Users
1. Register user1: `alice`
2. Create note for alice
3. Logout
4. Register user2: `bob`
5. Check notes list
6. ✅ **Expected**: Bob sees empty list (cannot see alice's notes)

### 6. Error Handling

#### Invalid Login
1. Try login with wrong password
2. ✅ **Expected**: Error message displayed, no redirect

#### Unauthorized Access
1. Logout
2. Try to access `/notes` directly via URL
3. ✅ **Expected**: Redirect to login page

#### Empty Fields
1. Try to create note with empty title
2. ✅ **Expected**: Validation error shown

### 7. UI/UX Testing

#### Responsive Design
1. Open app on desktop (1920x1080)
2. Resize to tablet (768px)
3. Resize to mobile (375px)
4. ✅ **Expected**: Layout adjusts properly, no broken UI

#### Loading States
1. Create note with slow network (Chrome DevTools throttling)
2. ✅ **Expected**: Loading spinner or disabled button during save

#### Navigation
1. Test all menu links
2. Use browser back/forward buttons
3. ✅ **Expected**: Navigation works smoothly, no broken routes

## Test Checklist

Before deployment, verify:
- [ ] User can register
- [ ] User can login/logout
- [ ] User can create notes
- [ ] User can edit notes
- [ ] User can delete notes
- [ ] User can create plans
- [ ] User can edit plans
- [ ] User can delete plans
- [ ] Data persists after refresh
- [ ] Users cannot see each other's data
- [ ] Validation errors show properly
- [ ] UI works on mobile/tablet/desktop
- [ ] Cloudflare tunnels work (if using)

## Reporting Issues

When you find a bug:
1. Note the steps to reproduce
2. Check browser console for errors (F12)
3. Check backend logs: `docker compose logs backend`
4. Document expected vs actual behavior
5. Fix or create issue for later

## Performance Testing

### Backend
```powershell
# Check API response times
Measure-Command { Invoke-RestMethod http://localhost:8000/notes -Headers @{"Authorization"="Bearer YOUR_TOKEN"} }
```

### Frontend
1. Open Chrome DevTools → Performance tab
2. Record page load
3. Check for slow operations
4. ✅ **Expected**: Page loads in < 2 seconds

## Security Testing

### SQL Injection
1. Try username: `admin' OR '1'='1`
2. ✅ **Expected**: Treated as literal string, no SQL injection

### XSS
1. Create note with content: `<script>alert('XSS')</script>`
2. ✅ **Expected**: Script not executed, displayed as text

### Authentication
1. Try accessing API without token:
   ```powershell
   Invoke-RestMethod http://localhost:8000/notes
   ```
2. ✅ **Expected**: 401 Unauthorized error

## Automated Backend Tests

Backend still has automated tests (37 tests):
```powershell
cd backend
python -m pytest tests/ -v
```

All backend tests should pass before deployment.

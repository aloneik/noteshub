# 🔒 What is CORS?

## Simple Explanation

**CORS (Cross-Origin Resource Sharing)** is a browser security mechanism that controls which websites can send requests to your API.

### 🎬 Real-World Example

Imagine:
- Your **backend (API)** runs at: `http://localhost:8000`
- Your **frontend (website)** runs at: `http://localhost:5173`

These are **different addresses** → the browser blocks requests between them!

```
❌ Without CORS:
Frontend (localhost:5173) --X--> Backend (localhost:8000)
         "Access blocked by CORS policy"

✅ With CORS:
Frontend (localhost:5173) --✓--> Backend (localhost:8000)
         "Access allowed"
```

## 🤔 When is This a Problem?

CORS triggers when **ANY** part of the address differs:

| What's Different | Example 1 | Example 2 | CORS? |
|------------------|----------|----------|-------|
| Port | `localhost:8000` | `localhost:5173` | ❌ Blocks |
| Domain | `example.com` | `api.example.com` | ❌ Blocks |
| Protocol | `http://site.com` | `https://site.com` | ❌ Blocks |
| Path Only | `site.com/api` | `site.com/users` | ✅ Allows |

## 🛡️ Why Do We Need This?

### Attack Example (without CORS):

```
1. You visit your bank's website: bank.com
2. You log in, browser saves cookies
3. You open a tab with hacker's site: evil-site.com
4. evil-site.com sends request to bank.com/transfer-money
5. Browser automatically includes your cookies
6. 💰 Money stolen!
```

**CORS blocks step 4** — evil-site.com cannot make requests to bank.com!

## ⚙️ How It Works in NoteHub

### 1. Backend Configuration (FastAPI)

```python
# app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React
        "http://localhost:5173",  # Vite
    ],
    allow_credentials=True,  # Allow cookies/auth
    allow_methods=["*"],     # GET, POST, PUT, DELETE
    allow_headers=["*"],     # Authorization, Content-Type
)
```

### 2. Frontend Requests

```javascript
// Frontend (React)
fetch('http://localhost:8000/api/notes', {
  headers: {
    'Authorization': 'Bearer your-token'
  }
})
.then(r => r.json())
.then(data => console.log('✅ Notes:', data))
```

## 🧪 Testing CORS

### Option 1: HTML Tester (Quick)

1. Start the backend:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. Open in browser:
   ```
   docs/cors-test.html
   ```

3. Click buttons and see results!

### Option 2: Browser DevTools

```javascript
// In browser console (F12)
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(data => console.log('✅ CORS works!', data))
  .catch(err => console.error('❌ CORS error:', err))
```

### Option 3: cURL

```bash
# Check CORS headers
curl -H "Origin: http://localhost:5173" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS \
     -v http://localhost:8000/api/notes
```

Expected headers:
```
< Access-Control-Allow-Origin: http://localhost:5173
< Access-Control-Allow-Credentials: true
< Access-Control-Allow-Methods: *
```

## 📝 Development vs Production

### Development (local development)

```python
# Automatically allowed:
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]
```

### Production (real server)

Set environment variable:

```bash
# .env or Environment Variables
CORS_ORIGINS=https://notehub.com,https://www.notehub.com
```

⚠️ **NEVER use `allow_origins=["*"]` in production!**

## 🐛 Common Issues

### Error: "blocked by CORS policy"

**Cause**: Frontend is on a port not allowed in the backend

**Solution**:
1. Check which port frontend is running on: `http://localhost:????`
2. Add this port to `app/core/config.py` → `CORS_ORIGINS`
3. Restart the backend

### Error: "credentials mode is 'include'"

**Cause**: Using `allow_origins=["*"]` with `allow_credentials=True`

**Solution**: Specify concrete domains instead of `*`

### Works locally, fails in production

**Problem**: Forgot to set `CORS_ORIGINS` on the server

**Solution**:
```bash
# Railway
railway variables set CORS_ORIGINS="https://notehub.com"

# Docker Compose
environment:
  - CORS_ORIGINS=https://notehub.com

# Heroku
heroku config:set CORS_ORIGINS="https://notehub.com"
```

## 📚 Additional Resources

- [MDN CORS Documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [FastAPI CORS Tutorial](https://fastapi.tiangolo.com/tutorial/cors/)
- Detailed documentation: `docs/cors-setup.md`
- Interactive tester: `docs/cors-test.html`

---

## 🎯 Quick Checklist

- ✅ CORS configured in `app/main.py`
- ✅ Required origins are allowed
- ✅ `allow_credentials=True` for authentication
- ✅ Tests pass (`pytest`)
- ✅ Backend running on correct port
- ✅ Frontend sending requests to correct address

**Done! Now your frontend can work with your API! 🚀**

# Documentation

This directory contains comprehensive documentation for the NoteHub project.

## 📚 Available Documentation

### CORS Configuration

- **[cors-explained.md](cors-explained.md)** - Beginner-friendly explanation of CORS
- **[cors-setup.md](cors-setup.md)** - Technical CORS configuration guide
- **[cors-test.html](cors-test.html)** - Interactive CORS testing tool
- **[CORS_SETUP_SUMMARY.md](CORS_SETUP_SUMMARY.md)** - Summary of CORS implementation

### GitHub Actions

- **[github-actions.md](github-actions.md)** - CI/CD pipeline documentation

## 🔒 Understanding CORS

**CORS (Cross-Origin Resource Sharing)** is essential when your frontend and backend run on different addresses.

### Quick Start

1. **Read the basics**: Start with [cors-explained.md](cors-explained.md)
2. **Configure**: Follow [cors-setup.md](cors-setup.md) for detailed setup
3. **Test**: Open [cors-test.html](cors-test.html) in your browser

### Common Scenarios

| Frontend | Backend | CORS Needed? |
|----------|---------|--------------|
| `localhost:3000` | `localhost:8000` | ✅ Yes (different ports) |
| `example.com` | `api.example.com` | ✅ Yes (different domains) |
| `example.com/app` | `example.com/api` | ❌ No (same origin) |

## 🧪 Testing CORS

### Option 1: HTML Tester (Recommended)

```bash
# 1. Start backend
cd backend
uvicorn app.main:app --reload

# 2. Open cors-test.html in browser
# 3. Click test buttons
```

### Option 2: Browser Console

```javascript
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(data => console.log('✅ CORS works!', data))
```

### Option 3: cURL

```bash
curl -H "Origin: http://localhost:5173" \
     -X OPTIONS \
     -v http://localhost:8000/health
```

## ⚙️ Current Configuration

The NoteHub backend has CORS pre-configured for common development scenarios:

```python
# Default allowed origins (development)
CORS_ORIGINS = [
    "http://localhost:3000",   # React (npm start)
    "http://localhost:5173",   # Vite (npm run dev)
    "http://localhost:5174",   # Vite alternative
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]
```

### Production Override

Set environment variable:

```bash
export CORS_ORIGINS="https://notehub.com,https://www.notehub.com"
```

## 🐛 Troubleshooting

### Error: "blocked by CORS policy"

1. Check backend is running: `http://localhost:8000/docs`
2. Verify frontend port matches allowed origins
3. See [cors-setup.md](cors-setup.md) troubleshooting section

### Need Help?

- Check [cors-explained.md](cors-explained.md) for conceptual understanding
- Review [cors-setup.md](cors-setup.md) for configuration details
- Use [cors-test.html](cors-test.html) to verify setup

## 📖 Additional Resources

- [MDN CORS Documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [FastAPI CORS Tutorial](https://fastapi.tiangolo.com/tutorial/cors/)
- [Understanding CORS (web.dev)](https://web.dev/cross-origin-resource-sharing/)

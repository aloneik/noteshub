# CORS Configuration Guide

## What is CORS?

**CORS (Cross-Origin Resource Sharing)** is a browser security mechanism that controls which websites can access your API.

### When is CORS needed?

CORS is required when frontend and backend run on different:
- **Domains**: `example.com` vs `api.example.com`
- **Ports**: `localhost:8000` vs `localhost:5173`
- **Protocols**: `http://` vs `https://`

## Current Configuration

### Development (default)

CORS is allowed for local frontends:
```python
CORS_ORIGINS = [
    "http://localhost:3000",   # React (npm start)
    "http://localhost:5173",   # Vite (npm run dev)
    "http://localhost:5174",   # Vite alternative port
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]
```

### Production

Set the `CORS_ORIGINS` environment variable:

```bash
# .env file or environment variables
CORS_ORIGINS=https://notehub.com,https://www.notehub.com,https://app.notehub.com
```

Or in Docker:
```yaml
environment:
  - CORS_ORIGINS=https://notehub.com,https://www.notehub.com
```

## CORS Settings

### Current Permissions

| Setting | Value | Description |
|---------|-------|-------------|
| `allow_origins` | See above | List of allowed origins |
| `allow_credentials` | `True` | Allow cookies and Authorization headers |
| `allow_methods` | `["*"]` | All HTTP methods (GET, POST, PUT, DELETE, etc.) |
| `allow_headers` | `["*"]` | All headers (Authorization, Content-Type, etc.) |

### Recommended for production

Restrict methods and headers:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
)
```

## Testing CORS

### From browser (DevTools Console)

```javascript
// Test CORS from frontend
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(data => console.log('✅ CORS works!', data))
  .catch(err => console.error('❌ CORS error:', err));
```

### With curl

```bash
# Check CORS headers
curl -H "Origin: http://localhost:5173" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Authorization" \
     -X OPTIONS \
     -v http://localhost:8000/api/notes
```

Should return headers:
```
Access-Control-Allow-Origin: http://localhost:5173
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: *
Access-Control-Allow-Headers: *
```

## Security

### ⚠️ Insecure

```python
# DO NOT use in production!
allow_origins=["*"]  # Allows ALL domains
```

### ✅ Secure

```python
# Explicitly specify allowed domains
allow_origins=[
    "https://notehub.com",
    "https://www.notehub.com",
]
```

## Troubleshooting

### Error: "blocked by CORS policy"

**Cause**: Frontend is not in the allowed origins list

**Solution**:
1. Check that frontend is running on an allowed port
2. Add frontend URL to `CORS_ORIGINS`
3. Restart backend

### Error: "credentials mode is 'include'"

**Cause**: `allow_credentials=True` requires specific origins (not `*`)

**Solution**: Specify exact domains instead of `*`

### Error in production

**Problem**: CORS works locally but not in production

**Solution**:
1. Ensure `CORS_ORIGINS` environment variable is set
2. Check that domains are specified with correct protocol (`https://`)
3. Check logs: `docker compose logs backend`

## Configuration Examples

### Kubernetes

```yaml
env:
  - name: CORS_ORIGINS
    value: "https://notehub.com,https://www.notehub.com"
```

### Docker Compose

```yaml
services:
  backend:
    environment:
      - CORS_ORIGINS=https://notehub.com,https://www.notehub.com
```

### Railway / Heroku

```bash
# CLI
railway variables set CORS_ORIGINS="https://notehub.com,https://www.notehub.com"
heroku config:set CORS_ORIGINS="https://notehub.com,https://www.notehub.com"
```

## Additional Resources

- [MDN CORS Documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [FastAPI CORS Middleware](https://fastapi.tiangolo.com/tutorial/cors/)
- [CORS Explained (web.dev)](https://web.dev/cross-origin-resource-sharing/)

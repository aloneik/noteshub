# Environment Variables for Render Deployment

This document lists all environment variables needed for deploying NoteHub backend on Render.com.

## Required Variables

### 1. DATABASE_URL
The PostgreSQL connection string. Render will automatically set this if you use the Blueprint (`render.yaml`).

**Format:**
```
postgresql+asyncpg://user:password@host:port/database
```

**Important:** Change `postgresql://` to `postgresql+asyncpg://` for asyncpg driver.

**Example:**
```
postgresql+asyncpg://notehub:mypassword@dpg-abc123.frankfurt-postgres.render.com/notehub
```

**How to get:**
1. Create PostgreSQL database in Render
2. Copy "Internal Database URL" from database dashboard
3. Replace `postgresql://` with `postgresql+asyncpg://`

---

### 2. SECRET_KEY
Secret key for JWT token signing. **Must be random and secure in production.**

**Generate secure key:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Example:**
```
SECRET_KEY=xK8vN3mP9qR2sT5wY7zA1bC4dE6fG8hJ0kL3mN5pQ8r
```

**Note:** In `render.yaml`, use `generateValue: true` to auto-generate.

---

### 3. CORS_ORIGINS
Comma-separated list of allowed frontend origins for CORS.

**Format:**
```
CORS_ORIGINS=origin1,origin2,origin3
```

**Example:**
```
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,https://notehub-frontend.vercel.app
```

**Important:**
- No spaces between URLs
- Include protocol (http:// or https://)
- No trailing slashes
- Update after deploying frontend

---

## Optional Variables

### Database Pool Settings
Fine-tune database connection pooling:

```
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
```

---

## Setting Variables in Render

### Method 1: Blueprint (render.yaml)
Variables are defined in `render.yaml`. Render applies them automatically.

### Method 2: Manual (Dashboard)
1. Open your Web Service in Render Dashboard
2. Go to **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Enter key and value
5. Click **"Save Changes"** (triggers redeploy)

---

## Example Configuration

Copy these to your Render Environment Variables section:

```
DATABASE_URL=postgresql+asyncpg://notehub:YOUR_PASSWORD@dpg-XXXXX.frankfurt-postgres.render.com/notehub
SECRET_KEY=xK8vN3mP9qR2sT5wY7zA1bC4dE6fG8hJ0kL3mN5pQ8r
CORS_ORIGINS=http://localhost:5173,https://your-frontend.vercel.app
```

Replace:
- `YOUR_PASSWORD` - from Render database credentials
- `dpg-XXXXX` - your database hostname
- `xK8v...` - your generated secret key
- `your-frontend` - your actual frontend URL

---

## Security Checklist

- [ ] SECRET_KEY is random and secure (not "secret")
- [ ] DATABASE_URL uses internal connection (not external)
- [ ] CORS_ORIGINS only includes your actual frontend URLs
- [ ] No sensitive data committed to Git

---

## Next Steps

After setting environment variables:
1. Deploy backend to Render
2. Test API at `https://your-backend.onrender.com/docs`
3. Update `CORS_ORIGINS` after deploying frontend
4. Configure custom domain (optional)

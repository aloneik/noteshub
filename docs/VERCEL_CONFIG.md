# Vercel Configuration Examples

## vercel.json

Create this file in `web_frontend/vercel.json`:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        },
        {
          "key": "Referrer-Policy",
          "value": "strict-origin-when-cross-origin"
        }
      ]
    },
    {
      "source": "/assets/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

## What it does

### Rewrites
- Routes all requests to `/index.html` for SPA routing
- Enables React Router to work on page refresh

### Headers
- **X-Content-Type-Options**: Prevents MIME type sniffing
- **X-Frame-Options**: Prevents clickjacking
- **X-XSS-Protection**: Enables XSS filter
- **Referrer-Policy**: Controls referrer information
- **Cache-Control**: Caches static assets for 1 year

## Usage

1. Copy the JSON above
2. Create `web_frontend/vercel.json`
3. Paste the content
4. Commit and push
5. Vercel will use this config on next deploy

## Optional: .vercelignore

Create `web_frontend/.vercelignore` to exclude files from deployment:

```
node_modules
.git
.env
.env.local
*.log
.DS_Store
README.md
```

## Environment Variables

Set in Vercel Dashboard → Settings → Environment Variables:

```
VITE_API_URL=https://notehub-backend.onrender.com
```

**Note**: Vite requires `VITE_` prefix for env vars!

## Custom Domain

To add custom domain:

1. Vercel Dashboard → Settings → Domains
2. Add your domain
3. Configure DNS:
   - Type: `CNAME`
   - Name: `@` or `www`
   - Value: `cname.vercel-dns.com`
4. Update backend CORS with new domain

## Deployment Triggers

Configure what triggers deployments:

- **Production**: Push to `master` branch
- **Preview**: Pull requests
- **Development**: Push to other branches

Settings → Git → Configure

## Build Settings Override

You can override in `vercel.json`:

```json
{
  "buildCommand": "npm run build",
  "installCommand": "npm ci",
  "outputDirectory": "dist"
}
```

Or use Dashboard → Settings → Build & Development Settings

## Regions

Vercel automatically deploys to multiple regions:
- Default: Global Edge Network
- Serverless Functions: Closest region to user

No configuration needed! ✅

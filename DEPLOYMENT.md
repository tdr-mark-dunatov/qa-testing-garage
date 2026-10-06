# 🚀 Deployment Guide - Webhook Pitstop

## Quick Deploy Options for Hackathon

### Option 1: Railway.app (Recommended - Easiest!)

**Why Railway:**
- ✅ Free tier available
- ✅ Auto HTTPS/SSL
- ✅ Auto-detects Docker
- ✅ One-click deploy
- ✅ Environment variables easy to set

**Steps:**
1. Push code to GitHub:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. Go to [Railway.app](https://railway.app) and sign in with GitHub

3. Click "New Project" → "Deploy from GitHub repo"

4. Select `webhook-pitstop` repo

5. Railway will auto-detect `docker-compose.yml` and deploy both services!

6. Set environment variable (optional):
   - `CORS_ALLOW_ALL=true` (for easier testing)

7. Get your public URL (e.g., `https://webhook-pitstop-production.up.railway.app`)

**Cost:** Free tier includes 500 hours/month

---

### Option 2: Render.com (Also Great!)

**Steps:**
1. Push to GitHub (same as above)

2. Go to [Render.com](https://render.com) and create account

3. Click "New +" → "Web Service"

4. Connect GitHub and select your repo

5. Configure:
   - **Name:** `webhook-pitstop-backend`
   - **Environment:** `Docker`
   - **Dockerfile Path:** `apps/api/Dockerfile`
   - **Port:** `8000`

6. Click "Create Web Service"

7. Repeat for frontend:
   - **Name:** `webhook-pitstop-frontend`
   - **Dockerfile Path:** `apps/web/Dockerfile`
   - **Port:** `80`

**Cost:** Free tier available (spins down after inactivity)

---

### Option 3: Local Docker (Testing)

**Quick Test:**
```bash
cd docker
docker-compose up --build
```

Access at: `http://localhost`

**Troubleshooting:**
- If port 80 is taken: Edit `docker-compose.yml` line 44 to `"8080:80"`
- Check logs: `docker-compose logs -f`
- Restart: `docker-compose down && docker-compose up --build`

---

### Option 4: DigitalOcean App Platform

**Steps:**
1. Push to GitHub

2. Go to [DigitalOcean Apps](https://cloud.digitalocean.com/apps)

3. Click "Create App" → "GitHub"

4. Select your repo

5. DigitalOcean auto-detects Docker and deploys

**Cost:** $5/month (no free tier, but very reliable)

---

## Environment Variables

### Backend (Optional)
```bash
# Database (default: SQLite)
DATABASE_URL=sqlite:///./data/pitstop.db

# CORS (for non-Docker deployments)
CORS_ALLOW_ALL=true
# or specify origins:
ALLOWED_ORIGINS=https://your-frontend.com,https://your-app.com
```

### Frontend (No env vars needed!)
Everything is auto-detected from `window.location`

---

## Testing After Deployment

1. **Health Check:**
   ```bash
   curl https://your-app.com/health
   ```
   Should return: `{"status":"🏁 Ready to race!","engine":"running"}`

2. **Create Pit Lane:**
   ```bash
   curl -X POST https://your-app.com/api/pit/new
   ```
   Returns your webhook URL!

3. **Test Webhook:**
   ```bash
   curl -X POST https://your-app.com/pit/YOUR-PIT-ID \
     -H "Content-Type: application/json" \
     -d '{"test": "hello from hackathon!"}'
   ```

4. **Open UI:**
   Go to `https://your-app.com` and create a pit lane!

---

## Hackathon Demo Tips

### 1. Show Real-time Updates
- Open your app in browser
- Create a pit lane
- In terminal, send requests with curl
- Watch them appear INSTANTLY (WebSockets!)

### 2. Racing Theme Demo
- Point out the car emojis 🏁⚡🔧
- "Pit Lane" = Webhook URL
- "Lap Time" = Response time
- Show the diagnostic dashboard

### 3. Use Case Demo
**QA Testing Scenario:**
```bash
# Simulate lender integration testing
curl -X POST https://your-app.com/pit/YOUR-PIT-ID \
  -H "Content-Type: application/json" \
  -H "X-Lender: HMF" \
  -d '{
    "dealId": "12345",
    "status": "APPROVED",
    "amount": 25000,
    "apr": 5.99
  }'
```

Show how QA can:
- Inspect exact headers
- View payload structure  
- Check response times
- Debug integration issues

### 4. Monorepo Extensibility
Show the README section about future apps:
- `apps/cli` - Command line tool
- `apps/mobile` - Mobile inspection
- `apps/admin` - Team collaboration

"Built as a monorepo so it's easy to add CLI tools, mobile apps, etc!"

---

## Troubleshooting

### WebSocket not connecting?
- Check browser console for errors
- Verify your deployment supports WebSockets (Railway & Render do!)
- Make sure HTTPS → WSS protocol is working

### CORS errors?
- Set `CORS_ALLOW_ALL=true` environment variable
- Or add your frontend domain to `ALLOWED_ORIGINS`

### Port conflicts locally?
Edit `docker-compose.yml`:
- Change line 24: `"8001:8000"` (backend)
- Change line 44: `"8080:80"` (frontend)

---

## Architecture Diagram for Judges

```
┌─────────────────┐
│   React + Vite  │
│   (Frontend)    │
│   Port 80       │
└────────┬────────┘
         │
    [nginx proxy]
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│  FastAPI        │◄────►│   SQLite     │
│  WebSocket      │      │   Database   │
│  Port 8000      │      │              │
└─────────────────┘      └──────────────┘
         │
         ▼
    [Real-time
     WebSocket
     Updates]
```

---

## What Makes This Special?

✅ **True Monorepo** - Not just a folder with two apps, uses npm workspaces + shared packages

✅ **Real-time** - WebSocket-powered live updates (not polling!)

✅ **Production-ready** - Docker, health checks, multi-stage builds

✅ **Racing Theme** - Perfect for automotive companies

✅ **QA Focused** - Built specifically for testing external integrations

✅ **Extensible** - Easy to add CLI, mobile, admin apps

---

## Quick Reference Commands

```bash
# Local Docker
cd docker && docker-compose up --build

# Build only backend
docker build -t webhook-pitstop-backend apps/api

# Build only frontend  
docker build -t webhook-pitstop-frontend apps/web

# Check Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart services
docker-compose restart backend
docker-compose restart frontend

# Stop everything
docker-compose down
```

---

🏁 **Happy Deploying! Good luck with the hackathon!** 🏁

# 🔧 Fix Railway Deployment Error

## Problem
Railway is showing: **"Error creating build plan with Railpack"**

This means Railway's auto-detection failed. Let's fix it!

---

## Solution: Configure Railway to Use Docker

### Option 1: In Railway Dashboard (Easiest)

1. **Go to your service in Railway**
2. **Click on "Settings" tab**
3. **Scroll to "Build & Deploy" section**
4. **Set "Build Command" to:**
   ```
   (leave empty - we use Dockerfile)
   ```
5. **Set "Start Command" to:**
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
6. **Set "Dockerfile Path" to:**
   ```
   Dockerfile
   ```
7. **Make sure "Docker" is selected as the build method**
8. **Click "Save"**
9. **Go to "Deployments" tab**
10. **Click "Redeploy" or trigger a new deployment**

---

### Option 2: Delete and Recreate Service

If Option 1 doesn't work:

1. **Delete the current service** (click X on service)
2. **Click "+ New" → "GitHub Repo"**
3. **Select your repository again**
4. **Before it starts building, go to Settings:**
   - Set build method to **"Docker"**
   - Set Dockerfile path to **"Dockerfile"**
5. **Then let it deploy**

---

### Option 3: Use Railway CLI

If you have Railway CLI installed:

```bash
railway link
railway variables set DATABASE_URL=<your-db-url>
railway variables set COINPAPRIKA_API_KEY=<your-key>
railway up
```

---

## Quick Fix Checklist

- [ ] Service Settings → Build method = **Docker**
- [ ] Dockerfile path = **Dockerfile**
- [ ] Start command = `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Environment variables are set
- [ ] Redeploy the service

---

## Still Not Working?

### Check These:

1. **Dockerfile exists** in root directory
2. **Dockerfile is valid** (no syntax errors)
3. **requirements.txt exists**
4. **All files are committed to GitHub**

### Common Issues:

**Issue**: Railway can't find Dockerfile
**Fix**: Make sure Dockerfile is in the root of your repo

**Issue**: Build fails during pip install
**Fix**: Check requirements.txt has all dependencies

**Issue**: Port binding error
**Fix**: Make sure you're using `$PORT` environment variable

---

## Alternative: Use Render.com

If Railway keeps having issues, try Render.com instead:

1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Environment: **Docker**
5. Deploy!

Render is often more reliable for Docker deployments.

---

## Need More Help?

Tell me:
1. What you see in Railway Settings
2. Any error messages
3. What you've tried

I'll help you fix it! 🚀


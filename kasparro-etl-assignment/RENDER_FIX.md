# 🔧 Fix Render Deployment - Dockerfile Not Found

## Problem
Render error: **"failed to read dockerfile: open Dockerfile: no such file or directory"**

This means Render can't find your Dockerfile. Let's fix it!

---

## ✅ Quick Fix

### Step 1: Make Sure Dockerfile is Committed to GitHub

The Dockerfile exists locally but might not be on GitHub. Let's check and push it:

```bash
cd /Users/pranavraj/kasparro-etl-assignment

# Check if Dockerfile is tracked
git status Dockerfile

# If it shows as untracked or modified, add and commit it:
git add Dockerfile
git add .dockerignore
git add railway.json
git commit -m "Add Dockerfile and deployment configs"
git push
```

### Step 2: Update Render Settings

1. **Go to Render Dashboard**
2. **Click on your service: "kasparro-backend-pranav-raj"**
3. **Go to "Settings" tab**
4. **Scroll to "Build & Deploy" section**
5. **Check these settings:**

   **Root Directory:** (leave empty or set to `/`)
   
   **Dockerfile Path:** `Dockerfile`
   
   **Docker Context:** `.` (or leave empty)
   
   **Build Command:** (leave empty - Dockerfile handles it)
   
   **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

6. **Click "Save Changes"**

### Step 3: Redeploy

1. **Go to "Events" tab**
2. **Click "Manual Deploy" → "Deploy latest commit"**
3. **Or push a new commit to trigger deployment**

---

## 🔍 Verify Dockerfile is on GitHub

1. Go to: `https://github.com/pranavraj28/kasparro-backend-pranav-raj`
2. Check if `Dockerfile` is visible in the root directory
3. If not, you need to commit and push it (see Step 1 above)

---

## 📝 Complete Render Configuration

Make sure your Render service has these settings:

### Build Settings:
- **Environment:** `Docker`
- **Dockerfile Path:** `Dockerfile`
- **Docker Context:** `.`
- **Root Directory:** (empty)

### Environment Variables:
Add these in Render → Settings → Environment:
```
DATABASE_URL=<from-postgres-service>
COINPAPRIKA_API_KEY=your_key_here
COINGECKO_API_KEY=your_key_here (optional)
ETL_INTERVAL_SECONDS=300
LOG_LEVEL=INFO
PORT=8000
```

### Start Command:
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

## 🚀 Step-by-Step: Push Dockerfile to GitHub

If Dockerfile is missing from GitHub:

```bash
# Navigate to your project
cd /Users/pranavraj/kasparro-etl-assignment

# Check git status
git status

# Add Dockerfile and related files
git add Dockerfile
git add .dockerignore
git add requirements.txt
git add app/
git add alembic/
git add alembic.ini
git add pyproject.toml

# Commit
git commit -m "Add complete project files for deployment"

# Push to GitHub
git push origin main
```

---

## ✅ After Pushing to GitHub

1. **Wait 30 seconds** for GitHub to update
2. **Go to Render Dashboard**
3. **Click "Manual Deploy" → "Deploy latest commit"**
4. **Watch the logs** - it should now find the Dockerfile!

---

## 🆘 Still Not Working?

### Check These:

1. **Dockerfile exists in GitHub root?**
   - Visit: `https://github.com/pranavraj28/kasparro-backend-pranav-raj/blob/main/Dockerfile`
   - If 404, it's not on GitHub

2. **Render is looking in the right place?**
   - Settings → Root Directory should be empty or `/`
   - Dockerfile Path should be `Dockerfile` (not `./Dockerfile`)

3. **Branch is correct?**
   - Make sure Render is deploying from `main` branch
   - Settings → Build → Branch: `main`

---

## 🎯 Quick Checklist

- [ ] Dockerfile exists locally
- [ ] Dockerfile is committed to git
- [ ] Dockerfile is pushed to GitHub
- [ ] Render settings: Environment = Docker
- [ ] Render settings: Dockerfile Path = `Dockerfile`
- [ ] Render settings: Root Directory = (empty)
- [ ] Environment variables are set
- [ ] Manual deploy triggered

---

## 📞 Need More Help?

If it's still not working:
1. Check if Dockerfile is visible on GitHub
2. Share what you see in Render Settings
3. Share the error message from logs

I'll help you fix it! 🚀


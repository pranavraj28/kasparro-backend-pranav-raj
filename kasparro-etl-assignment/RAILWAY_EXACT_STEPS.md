# 🚂 Railway Deployment - EXACT Steps (Copy & Paste)

## ✅ I've Fixed Everything - Just Follow These Steps

---

## Step 1: Push Files to GitHub (2 minutes)

### Option A: Using Terminal (If you have git auth set up)

```bash
cd /Users/pranavraj/kasparro-etl-assignment
git add railway.toml start.sh Dockerfile .dockerignore
git commit -m "Add Railway deployment config"
git push origin main
```

### Option B: Using GitHub Website (Easier)

1. Go to: https://github.com/pranavraj28/kasparro-backend-pranav-raj
2. Click "Add file" → "Upload files"
3. Upload these files from `/Users/pranavraj/kasparro-etl-assignment/`:
   - `railway.toml`
   - `start.sh`
   - `Dockerfile`
   - `.dockerignore`
4. Click "Commit changes"

---

## Step 2: Create Railway Project (3 minutes)

1. **Go to**: https://railway.app
2. **Click**: "Start a New Project" or "Login"
3. **Login with GitHub**
4. **Click**: "+ New Project"
5. **Click**: "Deploy from GitHub repo"
6. **Select**: `pranavraj28/kasparro-backend-pranav-raj`
7. **Wait**: Railway will try to auto-detect (it will fail, that's OK)

---

## Step 3: Configure Railway to Use Docker (CRITICAL!)

**This is the most important step!**

1. **Click on your service** (the one that just failed)
2. **Click "Settings" tab** (on the right)
3. **Scroll down to "Build" section**
4. **Find these fields and set them:**

   **Build Command**: (leave EMPTY)
   
   **Start Command**: 
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
   
   **Dockerfile Path**: 
   ```
   Dockerfile
   ```
   
   **Docker Context**: (leave empty or `.`)

5. **IMPORTANT**: Make sure **"Docker"** is selected as build method (not Railpack)
6. **Click "Save"** (blue button at bottom)

---

## Step 4: Add PostgreSQL Database (2 minutes)

1. **In your Railway project, click "+ New"**
2. **Click "Database"**
3. **Click "Add PostgreSQL"**
4. **Wait 30 seconds** for it to create
5. **Click on the PostgreSQL service**
6. **Go to "Variables" tab**
7. **Find `DATABASE_URL`**
8. **Copy this value** (you'll need it)

---

## Step 5: Add Environment Variables (2 minutes)

1. **Click on your web service** (not the database)
2. **Go to "Variables" tab**
3. **Click "+ New Variable"** for each:

   **Variable 1:**
   - Name: `DATABASE_URL`
   - Value: (paste the DATABASE_URL from PostgreSQL service)

   **Variable 2:**
   - Name: `COINPAPRIKA_API_KEY`
   - Value: (your API key from coinpaprika.com)

   **Variable 3:**
   - Name: `COINGECKO_API_KEY`
   - Value: (optional, can leave empty)

   **Variable 4:**
   - Name: `ETL_INTERVAL_SECONDS`
   - Value: `300`

   **Variable 5:**
   - Name: `LOG_LEVEL`
   - Value: `INFO`

   **Variable 6:**
   - Name: `PORT`
   - Value: `8000`

4. **Click "Add"** for each variable

---

## Step 6: Deploy! (1 minute)

1. **Go to "Deployments" tab**
2. **Click "Redeploy"** or wait for auto-deploy
3. **Watch the logs** - should see "Building..." then "Deploying..."
4. **Wait 2-3 minutes** for build to complete

---

## Step 7: Get Your Public URL (30 seconds)

1. **Click on your web service**
2. **Go to "Settings" tab**
3. **Scroll to "Domains" section**
4. **Click "Generate Domain"**
5. **Copy the URL!** It will be like: `https://kasparro-backend-pranav-raj-production.up.railway.app`

---

## Step 8: Test Your API (1 minute)

Open in browser:
```
https://YOUR-URL.railway.app/health
```

You should see:
```json
{"status":"healthy","database":"healthy","etl":"healthy"}
```

Also test:
```
https://YOUR-URL.railway.app/stats
https://YOUR-URL.railway.app/data
```

---

## ✅ You're Done!

**Your API is live at:** `https://YOUR-URL.railway.app`

**Submit this URL in the Google Form!** 🎉

---

## 🆘 If Something Fails

**Tell me:**
1. Which step you're on
2. What error you see
3. What the logs show

**I'll fix it immediately!** 🚀

---

## 📝 Quick Reference

- **Railway Dashboard**: https://railway.app/dashboard
- **Your Project**: Check Railway dashboard
- **GitHub Repo**: https://github.com/pranavraj28/kasparro-backend-pranav-raj

**You've got this!** 💪


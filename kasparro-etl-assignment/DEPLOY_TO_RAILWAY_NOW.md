# 🚂 Deploy to Railway - NOW (Everything Works Locally!)

## ✅ Local Test: PASSED!

Your app is working perfectly locally:
- ✅ API responding
- ✅ Database connected
- ✅ ETL running
- ✅ All endpoints working

**Now let's deploy to Railway!**

---

## Step 1: Push Files to GitHub (2 minutes)

### Option A: Using GitHub Website (Easiest)

1. Go to: https://github.com/pranavraj28/kasparro-backend-pranav-raj
2. Click "Add file" → "Upload files"
3. Upload these files from `/Users/pranavraj/kasparro-etl-assignment/`:
   - `railway.toml` ⭐ (IMPORTANT!)
   - `start.sh`
   - `Dockerfile`
   - `.dockerignore`
   - All files in `app/` folder
   - `requirements.txt`
   - `alembic/` folder
   - `alembic.ini`
4. Click "Commit changes"

### Option B: Using Terminal

```bash
cd /Users/pranavraj/kasparro-etl-assignment
git add .
git commit -m "Add all files for Railway deployment"
git push origin main
```

**If push fails**, use Option A (GitHub website).

---

## Step 2: Create/Configure Railway Project (5 minutes)

### 2.1: Create Project

1. Go to: https://railway.app
2. Login with GitHub
3. Click "+ New Project"
4. Click "Deploy from GitHub repo"
5. Select: `pranavraj28/kasparro-backend-pranav-raj`
6. Wait for it to try building (it will fail initially - that's OK)

### 2.2: Configure to Use Docker (CRITICAL!)

1. **Click on your service** (the one that failed)
2. **Click "Settings" tab** (on the right side)
3. **Scroll to "Build" section**
4. **Set these EXACTLY:**

   **Build Command**: (leave EMPTY - blank)
   
   **Start Command**: 
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
   
   **Dockerfile Path**: 
   ```
   Dockerfile
   ```
   
   **Docker Context**: (leave empty)

5. **IMPORTANT**: Make sure **"Docker"** is selected (NOT Railpack)
6. **Click "Save Changes"** (blue button)

### 2.3: If Files Are in Subdirectory

If your files are in `kasparro-etl-assignment/` folder:
- In Settings → **"Root Directory"** → Enter: `kasparro-etl-assignment`

---

## Step 3: Add PostgreSQL Database (2 minutes)

1. In Railway project, click **"+ New"**
2. Click **"Database"**
3. Click **"Add PostgreSQL"**
4. Wait 30 seconds for it to create
5. Click on the **PostgreSQL service**
6. Go to **"Variables" tab**
7. Find **`DATABASE_URL`**
8. **Copy this value** (you'll need it next)

---

## Step 4: Add Environment Variables (3 minutes)

1. Click on your **web service** (not the database)
2. Go to **"Variables" tab**
3. Click **"+ New Variable"** for each:

   **Variable 1:**
   - Name: `DATABASE_URL`
   - Value: (paste the DATABASE_URL from PostgreSQL service)

   **Variable 2:**
   - Name: `COINPAPRIKA_API_KEY`
   - Value: (your API key from https://coinpaprika.com/api/)

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

4. Click **"Add"** for each variable

---

## Step 5: Deploy! (2 minutes)

1. Go to **"Deployments" tab**
2. Click **"Redeploy"** or wait for auto-deploy
3. Watch the logs - should see:
   - "Building..."
   - "Deploying..."
   - "Application startup complete"
4. Wait 2-3 minutes for build to complete

---

## Step 6: Get Your Public URL (30 seconds)

1. Click on your **web service**
2. Go to **"Settings" tab**
3. Scroll to **"Domains" section**
4. Click **"Generate Domain"**
5. **Copy the URL!** 
   - Example: `https://kasparro-backend-pranav-raj-production.up.railway.app`

---

## Step 7: Test Your Deployed API (1 minute)

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
2. What error you see in Railway logs
3. What you see in Settings

**I'll help you fix it immediately!** 🚀

---

## 📝 Quick Checklist

- [ ] Files pushed to GitHub
- [ ] Railway project created
- [ ] Settings → Build method = **Docker** (not Railpack)
- [ ] Settings → Dockerfile Path = `Dockerfile`
- [ ] PostgreSQL database added
- [ ] Environment variables set
- [ ] Deployment successful
- [ ] Public URL obtained
- [ ] API tested and working

**You've got this!** 💪


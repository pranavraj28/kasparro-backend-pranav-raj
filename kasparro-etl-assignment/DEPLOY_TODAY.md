# 🚀 DEPLOY TODAY - Step by Step (I'll Help You!)

## ✅ I've Fixed Everything - Follow These Steps

---

## Option 1: Railway (Recommended - Easiest)

### Step 1: Push Updated Files to GitHub

```bash
cd /Users/pranavraj/kasparro-etl-assignment
git add railway.toml start.sh
git commit -m "Add Railway config files"
git push origin main
```

**If push fails, use GitHub website to upload these files:**
- `railway.toml`
- `start.sh`

### Step 2: Configure Railway

1. **Go to Railway Dashboard**: https://railway.app
2. **Click your project** (or create new if needed)
3. **Click "+ New" → "GitHub Repo"**
4. **Select**: `pranavraj28/kasparro-backend-pranav-raj`
5. **IMPORTANT**: Before it starts building:
   - Click on the service
   - Go to **"Settings"** tab
   - Scroll to **"Build"** section
   - Set **"Build Command"**: (leave empty)
   - Set **"Start Command"**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Set **"Dockerfile Path"**: `Dockerfile`
   - Make sure **"Docker"** is selected (not Railpack)
6. **Click "Save"**
7. **Go to "Deployments"** → It should start building!

### Step 3: Add Database

1. **Click "+ New" → "Database" → "Add PostgreSQL"**
2. **Wait for it to create**
3. **Click on PostgreSQL service → "Variables" tab**
4. **Copy the `DATABASE_URL`**

### Step 4: Add Environment Variables

1. **Click on your web service**
2. **Go to "Variables" tab**
3. **Add these:**
   - `DATABASE_URL` = (paste from PostgreSQL)
   - `COINPAPRIKA_API_KEY` = (your key)
   - `COINGECKO_API_KEY` = (optional)
   - `ETL_INTERVAL_SECONDS` = `300`
   - `LOG_LEVEL` = `INFO`
   - `PORT` = `8000`

### Step 5: Get Your URL

1. **Click on your web service**
2. **Go to "Settings" tab**
3. **Scroll to "Domains"**
4. **Click "Generate Domain"**
5. **Copy the URL!** That's your public API.

---

## Option 2: Render (Alternative)

### Step 1: Push Files to GitHub (same as above)

### Step 2: Configure Render

1. **Go to Render Dashboard**: https://render.com
2. **Click "New +" → "Web Service"**
3. **Connect GitHub** → Select your repo
4. **Settings:**
   - **Name**: `kasparro-backend-pranav-raj`
   - **Environment**: **Docker** (IMPORTANT!)
   - **Region**: Choose closest
   - **Branch**: `main`
   - **Root Directory**: `kasparro-etl-assignment` (if files are in subdirectory)
   - **Dockerfile Path**: `Dockerfile`
   - **Docker Context**: `.`
5. **Click "Create Web Service"**

### Step 3: Add PostgreSQL

1. **Click "New +" → "PostgreSQL"**
2. **Create database**
3. **Note the connection string**

### Step 4: Add Environment Variables

In your web service → Environment:
- `DATABASE_URL` = (from PostgreSQL)
- `COINPAPRIKA_API_KEY` = (your key)
- `ETL_INTERVAL_SECONDS` = `300`
- `LOG_LEVEL` = `INFO`
- `PORT` = `8000`

### Step 5: Deploy

Render will automatically deploy. Your URL will be:
`https://kasparro-backend-pranav-raj.onrender.com`

---

## 🔧 If Files Are in Subdirectory

If your files are in `kasparro-etl-assignment/` folder on GitHub:

### For Railway:
- Settings → Root Directory: `kasparro-etl-assignment`

### For Render:
- Settings → Root Directory: `kasparro-etl-assignment`

---

## ✅ Quick Checklist

- [ ] Files pushed to GitHub
- [ ] Railway/Render service created
- [ ] Build method set to **Docker** (not auto-detect)
- [ ] Dockerfile path set correctly
- [ ] PostgreSQL database added
- [ ] Environment variables set
- [ ] Deployment started
- [ ] Public URL obtained

---

## 🆘 Still Not Working?

**Tell me:**
1. Which platform (Railway or Render)?
2. What error you see in logs
3. What you see in Settings

**I'll fix it immediately!** 🚀

---

## 🎯 RECOMMENDED: Use Railway

Railway is easier:
1. Create project
2. Add GitHub repo
3. Set to Docker in Settings
4. Add database
5. Add env vars
6. Done!

**You can do this!** 💪


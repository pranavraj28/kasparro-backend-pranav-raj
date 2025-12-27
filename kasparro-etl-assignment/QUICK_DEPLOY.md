# ⚡ Quick Deploy - Copy & Paste Commands

## Option 1: Railway (Easiest - Recommended)

### 1. Put Code on GitHub

```bash
cd /Users/pranavraj/kasparro-etl-assignment
git init
git add .
git commit -m "Initial commit"

# Create repo on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/kasparro-backend-pranav-raj.git
git branch -M main
git push -u origin main
```

### 2. Deploy to Railway

1. Go to https://railway.app → Login with GitHub
2. Click "+ New Project" → "Deploy from GitHub repo"
3. Select your repo
4. Click "+ New" → "Database" → "Add PostgreSQL"
5. Click web service → "Variables" → Add:
   - `DATABASE_URL` = (from PostgreSQL service)
   - `COINPAPRIKA_API_KEY` = (your key)
   - `ETL_INTERVAL_SECONDS` = `300`
   - `LOG_LEVEL` = `INFO`
6. Settings → Domains → Generate Domain
7. **Done!** Your API is live.

---

## Option 2: Render (Also Easy)

### 1. Put Code on GitHub (same as above)

### 2. Deploy to Render

1. Go to https://render.com → Sign up with GitHub
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Settings:
   - Name: `kasparro-etl`
   - Environment: `Docker`
   - Click "Create Web Service"
5. Click "New +" → "PostgreSQL" → Create
6. In web service → Environment:
   - `DATABASE_URL` = (from PostgreSQL)
   - `COINPAPRIKA_API_KEY` = (your key)
   - `ETL_INTERVAL_SECONDS` = `300`
7. **Done!** Render gives you a URL automatically.

---

## 🎯 Which One?

**Railway** = Easier, faster setup
**Render** = Also easy, good free tier

**Both work great!** Choose either one.

---

## ✅ Test Your Deployment

```bash
# Replace with your URL
curl https://your-app.railway.app/health
curl https://your-app.railway.app/stats
curl https://your-app.railway.app/data
```

---

## 📝 What to Submit

1. GitHub repo URL
2. Public API URL (from Railway/Render)
3. Health check URL

**That's it!** 🚀


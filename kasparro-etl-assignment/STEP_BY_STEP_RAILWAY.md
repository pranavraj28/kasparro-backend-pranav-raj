# 🚂 Deploy to Railway.app - Step by Step (WITH SCREENSHOTS GUIDE)

This is the **EASIEST** way to deploy. Follow these steps exactly:

---

## Step 1: Prepare Your Code on GitHub

### 1.1 Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `kasparro-backend-pranav-raj`
3. Make it **Public** (for free tier)
4. Click "Create repository"

### 1.2 Push Your Code

Open terminal on your Mac and run:

```bash
cd /Users/pranavraj/kasparro-etl-assignment

# Initialize git if not done
git init
git add .
git commit -m "Initial commit - Kasparro ETL assignment"

# Add your GitHub repo (replace with your username)
git remote add origin https://github.com/YOUR_USERNAME/kasparro-backend-pranav-raj.git
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

---

## Step 2: Sign Up for Railway

1. Go to https://railway.app
2. Click "Login" or "Start a New Project"
3. Click "Login with GitHub"
4. Authorize Railway to access your GitHub

---

## Step 3: Create New Project

1. In Railway dashboard, click **"+ New Project"**
2. Select **"Deploy from GitHub repo"**
3. Select your repository: `kasparro-backend-pranav-raj`
4. Railway will start deploying automatically!

---

## Step 4: Add PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Click **"Database"**
3. Select **"Add PostgreSQL"**
4. Railway will create it automatically
5. **IMPORTANT**: Note the connection string (you'll need it)

---

## Step 5: Configure Environment Variables

1. Click on your **web service** (the one that's deploying)
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**
4. Add these variables one by one:

```
DATABASE_URL
```
- Value: Copy from your PostgreSQL service (click on it, copy the DATABASE_URL)

```
COINPAPRIKA_API_KEY
```
- Value: Your CoinPaprika API key (get from https://coinpaprika.com/api/)

```
COINGECKO_API_KEY
```
- Value: Your CoinGecko API key (optional, can leave empty)

```
ETL_INTERVAL_SECONDS
```
- Value: `300`

```
LOG_LEVEL
```
- Value: `INFO`

```
API_PORT
```
- Value: `8000`

5. Click **"Add"** for each variable

---

## Step 6: Get Your Public URL

1. Railway will automatically deploy
2. Once deployed, click on your service
3. Go to **"Settings"** tab
4. Scroll to **"Domains"**
5. Click **"Generate Domain"**
6. You'll get a URL like: `https://kasparro-etl-production.up.railway.app`
7. **Copy this URL!** This is your public API URL

---

## Step 7: Test Your API

Open a new browser tab and test:

```
https://YOUR-RAILWAY-URL.railway.app/health
```

You should see:
```json
{
  "status": "healthy",
  "database": "healthy",
  "etl": "healthy"
}
```

Also test:
```
https://YOUR-RAILWAY-URL.railway.app/stats
https://YOUR-RAILWAY-URL.railway.app/data
```

---

## Step 8: Set Up Cron Job (Scheduled ETL)

Railway doesn't support cron directly, but the ETL runs automatically every 5 minutes via the background task in `app/main.py`.

**This is already configured!** The ETL will run automatically.

---

## Step 9: View Logs

1. In Railway, click on your service
2. Go to **"Deployments"** tab
3. Click on the latest deployment
4. You'll see logs in real-time

---

## ✅ You're Done!

Your API is now live at: `https://YOUR-URL.railway.app`

### What to Submit:

1. **Public API URL**: `https://YOUR-URL.railway.app`
2. **GitHub Repository**: `https://github.com/YOUR_USERNAME/kasparro-backend-pranav-raj`
3. **Health Check**: `https://YOUR-URL.railway.app/health`
4. **Stats**: `https://YOUR-URL.railway.app/stats`

---

## 🆘 Troubleshooting

### Deployment Failed?
1. Check logs in Railway
2. Make sure all environment variables are set
3. Check that DATABASE_URL is correct

### API Not Responding?
1. Check if service is running (green status)
2. Check logs for errors
3. Verify environment variables

### Database Connection Error?
1. Make sure PostgreSQL service is running
2. Check DATABASE_URL is correct
3. Restart the web service

---

## 📝 Quick Reference

**Railway Dashboard**: https://railway.app/dashboard
**Your Project**: https://railway.app/project/YOUR_PROJECT_ID
**Documentation**: https://docs.railway.app

---

## 🎯 Next Steps

1. ✅ Deploy to Railway (you just did this!)
2. ✅ Test your API
3. ✅ Document your URL
4. ✅ Submit via Google Form: https://forms.gle/ouW6W1jH5wyRrnEX6

**You're all set!** 🚀


# 🆘 I Need Help Deploying - Complete Guide

Don't worry! I'll walk you through the **easiest** way step by step.

---

## 🎯 What We'll Do

We'll use **Railway.app** because it's:
- ✅ Free (no credit card needed)
- ✅ Easiest to use
- ✅ Automatic deployments
- ✅ Built-in database
- ✅ Takes 10 minutes

---

## 📋 Prerequisites

You need:
1. ✅ A GitHub account (free)
2. ✅ Your code (we have this!)
3. ✅ CoinPaprika API key (free, get from https://coinpaprika.com/api/)

---

## 🚀 Step-by-Step Instructions

### PART 1: Put Your Code on GitHub (5 minutes)

#### Step 1.1: Create GitHub Account (if you don't have one)
1. Go to https://github.com/signup
2. Sign up (it's free)
3. Verify your email

#### Step 1.2: Create Repository
1. Go to https://github.com/new
2. Repository name: `kasparro-backend-pranav-raj`
3. Make it **Public**
4. **Don't** initialize with README (we already have one)
5. Click "Create repository"

#### Step 1.3: Upload Your Code

**Option A: Using GitHub Website (Easiest)**
1. On the new repository page, you'll see instructions
2. Click "uploading an existing file"
3. Drag and drop your entire `kasparro-etl-assignment` folder
4. Scroll down, add commit message: "Initial commit"
5. Click "Commit changes"

**Option B: Using Terminal (If you prefer)**
```bash
cd /Users/pranavraj/kasparro-etl-assignment
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/kasparro-backend-pranav-raj.git
git push -u origin main
```

---

### PART 2: Deploy to Railway (5 minutes)

#### Step 2.1: Sign Up for Railway
1. Go to https://railway.app
2. Click "Start a New Project"
3. Click "Login with GitHub"
4. Authorize Railway

#### Step 2.2: Create Project
1. Click **"+ New Project"**
2. Click **"Deploy from GitHub repo"**
3. Find and select: `kasparro-backend-pranav-raj`
4. Railway will start deploying!

#### Step 2.3: Add Database
1. In your project, click **"+ New"**
2. Click **"Database"**
3. Click **"Add PostgreSQL"**
4. Wait for it to create (30 seconds)

#### Step 2.4: Get Database URL
1. Click on the **PostgreSQL** service
2. Go to **"Variables"** tab
3. Find **`DATABASE_URL`**
4. **Copy this value** (you'll need it)

#### Step 2.5: Configure Your App
1. Click on your **web service** (the one deploying)
2. Go to **"Variables"** tab
3. Add these variables:

**Variable 1:**
- Name: `DATABASE_URL`
- Value: (paste the DATABASE_URL from PostgreSQL service)

**Variable 2:**
- Name: `COINPAPRIKA_API_KEY`
- Value: (your API key from coinpaprika.com)

**Variable 3:**
- Name: `COINGECKO_API_KEY`
- Value: (optional, can leave empty or get from coingecko.com)

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

#### Step 2.6: Get Your Public URL
1. Click on your web service
2. Go to **"Settings"** tab
3. Scroll to **"Domains"**
4. Click **"Generate Domain"**
5. You'll get a URL like: `https://kasparro-etl-production-xxxx.up.railway.app`
6. **This is your public API URL!** Copy it.

---

### PART 3: Test Your Deployment (2 minutes)

#### Step 3.1: Test Health Endpoint
Open in browser:
```
https://YOUR-RAILWAY-URL.railway.app/health
```

You should see:
```json
{"status":"healthy","database":"healthy","etl":"healthy"}
```

#### Step 3.2: Test Stats Endpoint
```
https://YOUR-RAILWAY-URL.railway.app/stats
```

#### Step 3.3: Test Data Endpoint
```
https://YOUR-RAILWAY-URL.railway.app/data
```

---

## ✅ You're Done!

### What You Have Now:
1. ✅ Public API URL: `https://YOUR-URL.railway.app`
2. ✅ API is working
3. ✅ Database is connected
4. ✅ ETL is running automatically

### What to Submit:
1. **GitHub Repository URL**: `https://github.com/YOUR_USERNAME/kasparro-backend-pranav-raj`
2. **Public API URL**: `https://YOUR-URL.railway.app`
3. **Health Check**: `https://YOUR-URL.railway.app/health`

---

## 🆘 If Something Goes Wrong

### Problem: Deployment Failed
**Solution:**
1. Check the "Deployments" tab in Railway
2. Click on the failed deployment
3. Read the error message
4. Common issues:
   - Missing environment variables → Add them
   - Docker build failed → Check Dockerfile
   - Database connection → Check DATABASE_URL

### Problem: API Returns 404
**Solution:**
1. Make sure service is running (green status)
2. Check the URL is correct
3. Try `/health` endpoint first

### Problem: Database Error
**Solution:**
1. Make sure PostgreSQL service is running
2. Check DATABASE_URL is correct
3. Restart the web service

---

## 📞 Still Need Help?

If you're stuck at any step, tell me:
1. Which step you're on
2. What error you're seeing
3. What you've tried

I'll help you fix it!

---

## 🎯 Quick Checklist

- [ ] Code is on GitHub
- [ ] Railway account created
- [ ] Project deployed
- [ ] Database added
- [ ] Environment variables set
- [ ] Public URL generated
- [ ] API tested and working
- [ ] Ready to submit!

**You've got this!** 🚀


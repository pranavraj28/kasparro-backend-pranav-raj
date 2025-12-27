# 🔧 Fix Railway Error - requirements.txt Not Found

## Problem
Railway error: `"/requirements.txt" not found`

This means `requirements.txt` is not in your GitHub repo or Railway can't find it.

---

## ✅ Quick Fix

### Step 1: Verify File Exists Locally

The file exists at: `/Users/pranavraj/kasparro-etl-assignment/requirements.txt`

### Step 2: Upload to GitHub

**Option A: Using GitHub Website (Easiest)**

1. Go to: https://github.com/pranavraj28/kasparro-backend-pranav-raj
2. Check if `requirements.txt` is visible in the file list
3. If NOT visible:
   - Click "Add file" → "Upload files"
   - Upload `requirements.txt` from `/Users/pranavraj/kasparro-etl-assignment/`
   - Click "Commit changes"

**Option B: Using Terminal**

```bash
cd /Users/pranavraj/kasparro-etl-assignment
git add requirements.txt
git commit -m "Add requirements.txt"
git push origin main
```

### Step 3: Check Root Directory in Railway

If your files are in `kasparro-etl-assignment/` subdirectory:

1. Go to Railway → Your Service → Settings
2. Find "Root Directory" field
3. Set it to: `kasparro-etl-assignment`
4. Save
5. Redeploy

---

## 🔍 Verify on GitHub

1. Go to: https://github.com/pranavraj28/kasparro-backend-pranav-raj/blob/main/requirements.txt
2. If you see the file → It's on GitHub ✅
3. If 404 → Upload it (see Step 2)

---

## ✅ After Fixing

1. Wait 30 seconds for GitHub to update
2. Go to Railway → Deployments
3. Click "Redeploy" or wait for auto-deploy
4. Should work now!

---

## 🆘 Still Not Working?

**Check:**
1. Is `requirements.txt` visible on GitHub?
2. What's the Root Directory set to in Railway Settings?
3. Are files in root or subdirectory?

**Tell me and I'll help fix it!** 🚀


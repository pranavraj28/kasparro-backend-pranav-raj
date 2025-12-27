# 🚀 Easiest Deployment Options - Step by Step

I'll help you deploy this step by step. Here are the **easiest** options:

---

## Option 1: Railway.app (EASIEST - No Credit Card Needed) ⭐

Railway is free and very easy. Let's use this!

### Step 1: Sign Up
1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign up with GitHub (easiest)

### Step 2: Deploy
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Connect your GitHub account
4. Select your `kasparro-backend-pranav-raj` repository
5. Railway will auto-detect it's a Docker project

### Step 3: Add PostgreSQL
1. In Railway dashboard, click "+ New"
2. Select "Database" → "PostgreSQL"
3. Railway will create a database automatically

### Step 4: Set Environment Variables
In Railway, go to your service → Variables, add:
```
DATABASE_URL=<railway-provides-this-automatically>
COINPAPRIKA_API_KEY=your_key_here
COINGECKO_API_KEY=your_key_here
ETL_INTERVAL_SECONDS=300
LOG_LEVEL=INFO
```

### Step 5: Deploy!
Railway will automatically:
- Build your Docker image
- Deploy it
- Give you a public URL

### Step 6: Get Your URL
Railway will show you a URL like: `https://your-app.railway.app`

**That's it!** Your API will be at: `https://your-app.railway.app`

---

## Option 2: Render.com (Also Easy - Free Tier)

### Step 1: Sign Up
1. Go to https://render.com
2. Sign up with GitHub

### Step 2: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repo
3. Select your repository

### Step 3: Configure
- **Name**: kasparro-etl
- **Environment**: Docker
- **Region**: Choose closest to you
- **Branch**: main
- **Root Directory**: (leave empty)

### Step 4: Add PostgreSQL Database
1. Click "New +" → "PostgreSQL"
2. Create database
3. Note the connection string

### Step 5: Set Environment Variables
In your web service settings:
```
DATABASE_URL=<from-postgres-service>
COINPAPRIKA_API_KEY=your_key
COINGECKO_API_KEY=your_key
ETL_INTERVAL_SECONDS=300
```

### Step 6: Deploy
Click "Create Web Service" - Render will deploy automatically!

---

## Option 3: Fly.io (Free Tier Available)

### Step 1: Install Fly CLI
```bash
# On Mac
curl -L https://fly.io/install.sh | sh

# Or download from https://fly.io/docs/getting-started/installing-flyctl/
```

### Step 2: Sign Up
```bash
fly auth signup
```

### Step 3: Deploy
```bash
cd /Users/pranavraj/kasparro-etl-assignment
fly launch
# Follow prompts
```

### Step 4: Add Database
```bash
fly postgres create --name kasparro-db
fly attach --app kasparro-etl kasparro-db
```

### Step 5: Set Secrets
```bash
fly secrets set COINPAPRIKA_API_KEY=your_key
fly secrets set COINGECKO_API_KEY=your_key
```

---

## Option 4: AWS EC2 (If You Have AWS Account)

### Step 1: Launch Instance
1. Go to https://console.aws.amazon.com/ec2
2. Click "Launch Instance"
3. Name: `kasparro-etl`
4. AMI: Ubuntu Server 22.04 LTS
5. Instance type: t3.micro (free tier) or t3.small
6. Key pair: Create new or use existing
7. Network settings:
   - Allow SSH (port 22) from your IP
   - Allow HTTP (port 8000) from anywhere
8. Click "Launch Instance"

### Step 2: Connect
```bash
# Download your key pair
# Then connect:
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@YOUR_EC2_IP
```

### Step 3: On the Server
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone your repo
git clone https://github.com/your-username/kasparro-backend-pranav-raj.git
cd kasparro-backend-pranav-raj

# Create .env
nano .env
# Add your API keys, save (Ctrl+X, Y, Enter)

# Deploy
chmod +x deploy.sh
./deploy.sh
```

---

## 🎯 Which Should You Choose?

**Easiest**: Railway.app or Render.com
- No command line needed
- Free tier available
- Automatic deployments
- Built-in databases

**Recommended for beginners**: Railway.app
- Simplest interface
- GitHub integration
- Free tier
- No credit card needed

---

## 📝 Quick Checklist

After deployment, you need:
- [ ] Public URL (e.g., https://your-app.railway.app)
- [ ] API working (test `/health` endpoint)
- [ ] ETL running (check `/stats` endpoint)
- [ ] Document the URL for submission

---

## 🆘 Need More Help?

Tell me which option you want to try, and I'll give you even more detailed steps!

**I recommend starting with Railway.app - it's the easiest!** 🚀


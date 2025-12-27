# 🚀 Cloud Deployment Guide

This guide will help you deploy the Kasparro ETL system to AWS, GCP, or Azure.

---

## Option 1: AWS EC2 Deployment

### Step 1: Launch EC2 Instance

1. Go to AWS Console → EC2 → Launch Instance
2. Choose:
   - **AMI**: Ubuntu Server 22.04 LTS
   - **Instance Type**: t3.medium or larger (2GB+ RAM)
   - **Storage**: 20GB minimum
   - **Security Group**: 
     - Allow SSH (port 22) from your IP
     - Allow HTTP (port 80) from anywhere
     - Allow Custom TCP (port 8000) from anywhere (or use port 80 with nginx)

### Step 2: Connect to Instance

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

### Step 3: Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker ubuntu
newgrp docker

# Install Git
sudo apt install -y git
```

### Step 4: Clone and Setup

```bash
# Clone repository
git clone https://github.com/your-username/kasparro-backend-pranav-raj.git
cd kasparro-backend-pranav-raj

# Create .env file
nano .env
```

Add your configuration:
```bash
DATABASE_URL=postgresql://postgres:postgres@db:5432/crypto_etl
API_HOST=0.0.0.0
API_PORT=8000
ETL_INTERVAL_SECONDS=300
ETL_BATCH_SIZE=100
LOG_LEVEL=INFO
COINPAPRIKA_API_KEY=your_coinpaprika_key_here
COINGECKO_API_KEY=your_coingecko_key_here
CSV_SOURCE_PATH=data/sample.csv
```

### Step 5: Start Services

```bash
# Build and start
make up

# Verify
curl http://localhost:8000/health
```

### Step 6: Set Up Nginx (Optional but Recommended)

```bash
# Install Nginx
sudo apt install -y nginx

# Create config
sudo nano /etc/nginx/sites-available/kasparro-etl
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com or your-ec2-ip;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/kasparro-etl /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 7: Set Up Cron for Scheduled ETL

```bash
# Edit crontab
crontab -e

# Add this line (runs every 5 minutes)
*/5 * * * * cd /home/ubuntu/kasparro-backend-pranav-raj && docker-compose restart api >> /var/log/etl-cron.log 2>&1
```

### Step 8: Set Up CloudWatch Logs

```bash
# Install CloudWatch agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i amazon-cloudwatch-agent.deb

# Configure (interactive)
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard

# Start agent
sudo systemctl start amazon-cloudwatch-agent
sudo systemctl enable amazon-cloudwatch-agent
```

### Step 9: Verify Deployment

```bash
# Test API
curl http://your-ec2-ip:8000/health
curl http://your-ec2-ip:8000/stats
curl http://your-ec2-ip:8000/data

# Check logs
docker-compose logs -f api

# Check cron
tail -f /var/log/etl-cron.log
```

---

## Option 2: GCP Compute Engine Deployment

### Step 1: Create VM Instance

1. Go to GCP Console → Compute Engine → VM Instances
2. Create instance:
   - **Name**: kasparro-etl
   - **Machine type**: e2-medium or larger
   - **Boot disk**: Ubuntu 22.04 LTS
   - **Firewall**: Allow HTTP and HTTPS traffic

### Step 2: Connect and Setup

```bash
# Connect via SSH (use GCP console or gcloud)
gcloud compute ssh kasparro-etl

# Install Docker (same as AWS steps)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo usermod -aG docker $USER
newgrp docker
```

### Step 3: Deploy Application

```bash
# Clone repository
git clone https://github.com/your-username/kasparro-backend-pranav-raj.git
cd kasparro-backend-pranav-raj

# Create .env file
nano .env
# (Add same configuration as AWS)

# Start services
make up
```

### Step 4: Set Up Cloud Scheduler

1. Go to GCP Console → Cloud Scheduler
2. Create job:
   - **Name**: etl-run
   - **Frequency**: `*/5 * * * *` (every 5 minutes)
   - **Target**: HTTP
   - **URL**: `http://your-vm-ip:8000/stats` (or create a trigger endpoint)
   - **Method**: GET

### Step 5: Set Up Stackdriver Logging

```bash
# Install Stackdriver agent
curl -sSO https://dl.google.com/cloudagents/add-logging-agent-repo.sh
sudo bash add-logging-agent-repo.sh
sudo apt-get update
sudo apt-get install -y google-fluentd
sudo systemctl start google-fluentd
sudo systemctl enable google-fluentd
```

---

## Option 3: Azure VM Deployment

### Step 1: Create VM

1. Go to Azure Portal → Virtual Machines → Create
2. Choose:
   - **Image**: Ubuntu Server 22.04 LTS
   - **Size**: Standard_B2s or larger
   - **Networking**: Allow SSH and HTTP ports

### Step 2: Connect and Setup

```bash
# Connect via SSH
ssh azureuser@your-vm-ip

# Install Docker (same steps as AWS/GCP)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
# ... (same as above)
```

### Step 3: Deploy Application

```bash
# Clone and setup (same as above)
git clone https://github.com/your-username/kasparro-backend-pranav-raj.git
cd kasparro-backend-pranav-raj
# ... (same as above)
```

### Step 4: Set Up Azure Automation

1. Go to Azure Portal → Automation Accounts
2. Create runbook to trigger ETL
3. Schedule with Azure Scheduler

### Step 5: Set Up Application Insights

```bash
# Install Application Insights agent
# Follow Azure documentation for your stack
```

---

## 🔧 Common Setup Steps (All Platforms)

### 1. Environment Variables

Create `.env` file:
```bash
DATABASE_URL=postgresql://postgres:postgres@db:5432/crypto_etl
API_HOST=0.0.0.0
API_PORT=8000
ETL_INTERVAL_SECONDS=300
ETL_BATCH_SIZE=100
LOG_LEVEL=INFO
COINPAPRIKA_API_KEY=your_key_here
COINGECKO_API_KEY=your_key_here
CSV_SOURCE_PATH=data/sample.csv
```

### 2. Start Services

```bash
make up
```

### 3. Verify

```bash
curl http://localhost:8000/health
curl http://localhost:8000/stats
curl http://localhost:8000/data
```

### 4. Set Up Logging

- **AWS**: CloudWatch Logs
- **GCP**: Stackdriver Logging
- **Azure**: Application Insights

### 5. Set Up Monitoring

- **AWS**: CloudWatch Metrics
- **GCP**: Cloud Monitoring
- **Azure**: Azure Monitor

---

## 📝 Post-Deployment Checklist

- [ ] Services running (`make up` successful)
- [ ] API accessible (curl returns 200)
- [ ] ETL running automatically
- [ ] Cron job scheduled (or Cloud Scheduler)
- [ ] Logs visible in cloud console
- [ ] Public URL documented in README
- [ ] Smoke test completed

---

## 🆘 Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs

# Check database
docker-compose exec db psql -U postgres -c "SELECT 1"
```

### API not accessible
```bash
# Check firewall rules
# Check security groups
# Verify port 8000 is open
```

### ETL not running
```bash
# Check logs
docker-compose logs api

# Manually trigger
docker-compose exec api python -c "from app.services.etl_runner import ETLRunner; from app.core.db import SessionLocal; ETLRunner(SessionLocal()).run_all()"
```

---

## 📞 Support

If you encounter issues:
1. Check logs: `docker-compose logs -f`
2. Verify environment variables
3. Check database connectivity
4. Review firewall/security group settings

Good luck with deployment! 🚀


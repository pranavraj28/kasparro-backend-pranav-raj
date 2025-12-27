# 🚀 Quick Cloud Deployment Guide

## Option 1: Automated Deployment (Easiest)

### Step 1: Launch a Cloud VM

**AWS EC2:**
1. Go to AWS Console → EC2 → Launch Instance
2. Choose Ubuntu 22.04 LTS
3. Select t3.medium or larger
4. Configure security group: Allow ports 22 (SSH), 8000 (API), 80 (HTTP)
5. Launch and connect via SSH

**GCP Compute Engine:**
1. Go to GCP Console → Compute Engine → Create Instance
2. Choose Ubuntu 22.04 LTS
3. Select e2-medium or larger
4. Allow HTTP and HTTPS traffic
5. Connect via SSH

**Azure VM:**
1. Go to Azure Portal → Virtual Machines → Create
2. Choose Ubuntu 22.04 LTS
3. Select Standard_B2s or larger
4. Allow SSH and HTTP ports
5. Connect via SSH

### Step 2: Run Deployment Script

```bash
# On your cloud VM, run:
git clone https://github.com/your-username/kasparro-backend-pranav-raj.git
cd kasparro-backend-pranav-raj
chmod +x deploy.sh
./deploy.sh
```

The script will:
- ✅ Install Docker and Docker Compose
- ✅ Set up environment
- ✅ Deploy the application
- ✅ Configure cron job
- ✅ Show you the public API URL

### Step 3: Add API Keys

Edit `.env` file and add your API keys:
```bash
nano .env
# Add:
COINPAPRIKA_API_KEY=your_key_here
COINGECKO_API_KEY=your_key_here
```

Restart services:
```bash
docker-compose restart api
```

### Step 4: Test

```bash
# Get your public IP
curl ifconfig.me

# Test API
curl http://YOUR_PUBLIC_IP:8000/health
curl http://YOUR_PUBLIC_IP:8000/stats
```

---

## Option 2: Terraform Deployment (AWS)

### Prerequisites
- AWS CLI configured
- Terraform installed

### Steps

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your key pair name

terraform init
terraform plan
terraform apply
```

After deployment:
```bash
# Get the instance IP from output
# SSH into the instance
# Clone your repo and run deploy.sh
```

---

## Option 3: CloudFormation (AWS)

### Steps

```bash
# Via AWS CLI
aws cloudformation create-stack \
  --stack-name kasparro-etl \
  --template-body file://cloudformation/kasparro-etl.yaml \
  --parameters ParameterKey=KeyPairName,ParameterValue=your-key-pair-name \
  --capabilities CAPABILITY_IAM

# Or via AWS Console:
# 1. Go to CloudFormation
# 2. Create stack
# 3. Upload cloudformation/kasparro-etl.yaml
# 4. Fill in parameters
# 5. Create stack
```

---

## Option 4: Manual Deployment

Follow the detailed steps in `DEPLOYMENT_GUIDE.md`

---

## 🔥 Fastest Method (5 minutes)

If you already have a cloud VM:

```bash
# 1. SSH into your VM
ssh user@your-vm-ip

# 2. Clone and deploy
git clone https://github.com/your-username/kasparro-backend-pranav-raj.git
cd kasparro-backend-pranav-raj
chmod +x deploy.sh
./deploy.sh

# 3. Add API keys to .env
nano .env
# Add your keys, save, then:
docker-compose restart api

# 4. Test
curl http://$(curl -s ifconfig.me):8000/health
```

---

## 📝 Post-Deployment Checklist

- [ ] Application is running (`docker-compose ps`)
- [ ] API is accessible (`curl http://PUBLIC_IP:8000/health`)
- [ ] Cron job is set up (`crontab -l`)
- [ ] API keys are configured (`.env` file)
- [ ] Logs are working (`docker-compose logs`)
- [ ] ETL is running (check `/stats` endpoint)

---

## 🆘 Troubleshooting

### Can't access API
- Check security group/firewall allows port 8000
- Check if services are running: `docker-compose ps`
- Check logs: `docker-compose logs api`

### ETL not running
- Check logs: `docker-compose logs api`
- Verify cron job: `crontab -l`
- Manually trigger: `docker-compose restart api`

### Database issues
- Check database: `docker-compose exec db psql -U postgres -c "SELECT 1"`
- Restart database: `docker-compose restart db`

---

## ✅ You're Done!

Once deployed:
1. Document your public API URL
2. Test all endpoints
3. Submit via Google Form with the URL

Good luck! 🚀


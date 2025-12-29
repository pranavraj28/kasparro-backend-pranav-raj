#!/bin/bash
# Automated deployment script for Kasparro ETL System
# Supports: AWS EC2, GCP Compute Engine, Azure VM

set -e

echo "🚀 Kasparro ETL - Cloud Deployment Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running on a cloud instance
detect_cloud() {
    if curl -s --max-time 2 http://169.254.169.254/latest/meta-data/ > /dev/null 2>&1; then
        echo "AWS"
    elif curl -s --max-time 2 -H "Metadata-Flavor: Google" http://169.254.169.254/computeMetadata/v1/ > /dev/null 2>&1; then
        echo "GCP"
    elif curl -s --max-time 2 -H "Metadata: true" http://169.254.169.254/metadata/instance?api-version=2021-02-01 > /dev/null 2>&1; then
        echo "Azure"
    else
        echo "Local"
    fi
}

CLOUD=$(detect_cloud)
echo -e "${GREEN}Detected cloud provider: ${CLOUD}${NC}"
echo ""

# Check prerequisites
check_prerequisites() {
    echo "🔍 Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker not found. Installing...${NC}"
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
        echo -e "${GREEN}✅ Docker installed${NC}"
    else
        echo -e "${GREEN}✅ Docker found${NC}"
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}❌ Docker Compose not found. Installing...${NC}"
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
        echo -e "${GREEN}✅ Docker Compose installed${NC}"
    else
        echo -e "${GREEN}✅ Docker Compose found${NC}"
    fi
    
    if ! command -v git &> /dev/null; then
        echo -e "${RED}❌ Git not found. Installing...${NC}"
        sudo apt-get update
        sudo apt-get install -y git
        echo -e "${GREEN}✅ Git installed${NC}"
    else
        echo -e "${GREEN}✅ Git found${NC}"
    fi
    
    echo ""
}

# Setup environment
setup_environment() {
    echo "⚙️  Setting up environment..."
    
    if [ ! -f .env ]; then
        echo "Creating .env file from template..."
        cat > .env << EOF
# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/crypto_etl

# API
API_HOST=0.0.0.0
API_PORT=8000

# ETL
ETL_INTERVAL_SECONDS=300
ETL_BATCH_SIZE=100

# Failure injection (for testing)
FAIL_AFTER_N_RECORDS=

# Logging
LOG_LEVEL=INFO

# External APIs - ADD YOUR KEYS HERE
COINPAPRIKA_API_KEY=
COINGECKO_API_KEY=

# CSV Source
CSV_SOURCE_PATH=data/sample.csv
EOF
        echo -e "${YELLOW}⚠️  Please edit .env file and add your API keys${NC}"
        echo "Press Enter to continue after adding keys, or Ctrl+C to exit..."
        read
    else
        echo -e "${GREEN}✅ .env file exists${NC}"
    fi
    
    echo ""
}

# Deploy application
deploy_application() {
    echo "🚀 Deploying application..."
    
    # Stop existing containers
    docker-compose down 2>/dev/null || true
    
    # Build and start
    echo "Building Docker images..."
    docker-compose build
    
    echo "Starting services..."
    docker-compose up -d
    
    echo "Waiting for services to be ready..."
    sleep 10
    
    # Health check
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Application is healthy!${NC}"
    else
        echo -e "${RED}❌ Application health check failed${NC}"
        echo "Check logs with: docker-compose logs"
        exit 1
    fi
    
    echo ""
}

# Setup cron job
setup_cron() {
    echo "⏰ Setting up cron job for scheduled ETL runs..."
    
    CRON_CMD="cd $(pwd) && docker-compose restart api >> /var/log/etl-cron.log 2>&1"
    CRON_JOB="*/5 * * * * $CRON_CMD"
    
    # Check if cron job already exists
    if crontab -l 2>/dev/null | grep -q "$CRON_CMD"; then
        echo -e "${GREEN}✅ Cron job already exists${NC}"
    else
        (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
        echo -e "${GREEN}✅ Cron job added (runs every 5 minutes)${NC}"
    fi
    
    echo ""
}

# Get public IP
get_public_ip() {
    case $CLOUD in
        "AWS")
            PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
            ;;
        "GCP")
            PUBLIC_IP=$(curl -s -H "Metadata-Flavor: Google" http://169.254.169.254/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip)
            ;;
        "Azure")
            PUBLIC_IP=$(curl -s -H "Metadata: true" http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/publicIpAddress?api-version=2021-02-01 | grep -oP '"publicIpAddress":"\K[^"]+')
            ;;
        *)
            PUBLIC_IP=$(curl -s ifconfig.me || curl -s icanhazip.com || echo "unknown")
            ;;
    esac
    
    echo "$PUBLIC_IP"
}

# Main deployment
main() {
    echo "Starting deployment process..."
    echo ""
    
    check_prerequisites
    setup_environment
    deploy_application
    setup_cron
    
    PUBLIC_IP=$(get_public_ip)
    
    echo "=========================================="
    echo -e "${GREEN}✅ Deployment Complete!${NC}"
    echo "=========================================="
    echo ""
    echo "📊 Service Information:"
    echo "  - Local API: http://localhost:8000"
    echo "  - Public API: http://${PUBLIC_IP}:8000"
    echo "  - Health Check: http://${PUBLIC_IP}:8000/health"
    echo "  - API Docs: http://${PUBLIC_IP}:8000/docs"
    echo ""
    echo "📝 Next Steps:"
    echo "  1. Test API: curl http://${PUBLIC_IP}:8000/health"
    echo "  2. Check logs: docker-compose logs -f"
    echo "  3. View stats: curl http://${PUBLIC_IP}:8000/stats"
    echo ""
    echo "⚠️  Important:"
    echo "  - Make sure port 8000 is open in your firewall/security group"
    echo "  - Add your API keys to .env file if not already done"
    echo "  - Cron job runs ETL every 5 minutes"
    echo ""
}

# Run main function
main


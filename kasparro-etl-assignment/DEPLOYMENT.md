# 🌐 Cloud Deployment Documentation

## Production Environment

**Live URL:** https://kasparro-backend-agwk.onrender.com  
**Platform:** Render  
**Service Type:** Web Service (Docker Container)  
**Region:** US-East  
**Database:** PostgreSQL (Render Managed Database)  
**Status:** ✅ Operational

---

## Architecture
```
GitHub Repository (main branch)
         ↓
    [Push Trigger]
         ↓
   Render Build System
         ↓
   Docker Image Build
         ↓
   Container Deployment
         ↓
   PostgreSQL Database
         ↓
   Public HTTPS Endpoint
```

---

## Deployment Process

### 1. **Automatic Deployment**
- Connected to GitHub repository
- Auto-deploys on push to `main` branch
- Build time: ~3-5 minutes
- Zero-downtime deployments

### 2. **Build Configuration**
```yaml
# render.yaml
services:
  - type: web
    name: kasparro-backend
    env: docker
    dockerfilePath: ./Dockerfile
    healthCheckPath: /health
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: kasparro-db
          property: connectionString
```

### 3. **Docker Configuration**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Verification Steps

### 1. Health Check ✅
```bash
curl https://kasparro-backend-agwk.onrender.com/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-12-31T12:00:00Z"
}
```

### 2. Data API ✅
```bash
curl "https://kasparro-backend-agwk.onrender.com/data?page=1&page_size=5"
```

**Expected Response:**
```json
{
  "data": [
    {
      "id": 1,
      "symbol": "BTC",
      "name": "Bitcoin",
      "price_usd": 45000.00,
      "source": "coinpaprika"
    },
    ...
  ],
  "metadata": {
    "request_id": "abc-123",
    "api_latency_ms": 42,
    "page": 1,
    "page_size": 5,
    "total": 1500
  }
}
```

### 3. Stats Endpoint ✅
```bash
curl https://kasparro-backend-agwk.onrender.com/stats
```

**Expected Response:**
```json
{
  "total_records": 1500,
  "last_run": {
    "timestamp": "2025-12-31T10:00:00Z",
    "status": "success",
    "duration_ms": 5432
  },
  "sources": {
    "coinpaprika": 500,
    "coingecko": 500,
    "csv": 500
  }
}
```

### 4. API Documentation ✅
Open in browser: https://kasparro-backend-agwk.onrender.com/docs

**Expected:** Interactive Swagger UI with all endpoints documented

---

## Environment Variables

Configured in Render Dashboard (Settings → Environment):

| Variable | Description | Type |
|----------|-------------|------|
| `DATABASE_URL` | PostgreSQL connection string | Secret |
| `COINPAPRIKA_API_KEY` | CoinPaprika API authentication | Secret |
| `COINGECKO_API_KEY` | CoinGecko API authentication | Secret |
| `ENVIRONMENT` | Deployment environment | Plain |
| `LOG_LEVEL` | Logging verbosity | Plain |

**Security:** All secrets are encrypted and not visible in logs.

---

## Database Configuration

### PostgreSQL Details
- **Service:** Render PostgreSQL
- **Version:** 15
- **Connection:** Internal private network
- **Backups:** Daily automatic backups
- **Storage:** 1GB SSD

### Database Schema
```sql
-- Normalized assets table
CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    name VARCHAR(100),
    price_usd DECIMAL(20, 8),
    source VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(symbol, source)
);

-- Checkpoints for incremental ingestion
CREATE TABLE checkpoints (
    id SERIAL PRIMARY KEY,
    source VARCHAR(50) NOT NULL,
    last_processed_id VARCHAR(100),
    last_run TIMESTAMP,
    status VARCHAR(20),
    UNIQUE(source)
);
```

---

## Monitoring & Health Checks

### 1. Automated Health Checks
- **Frequency:** Every 5 minutes
- **Endpoint:** `/health`
- **Timeout:** 30 seconds
- **Action on Failure:** Auto-restart after 3 consecutive failures

### 2. Logging
- **Format:** Structured JSON logs
- **Retention:** 7 days on free tier
- **Access:** Render Dashboard → Logs

**Example Log:**
```json
{
  "timestamp": "2025-12-31T12:00:00Z",
  "level": "INFO",
  "message": "ETL run completed",
  "records_processed": 150,
  "duration_ms": 5432,
  "source": "coinpaprika"
}
```

### 3. Metrics
Available in Render Dashboard:
- CPU usage
- Memory usage
- Request count
- Response times
- Error rates

---

## ETL Scheduling

### Current Implementation
**Trigger:** Container startup

When the container starts:
1. Database connection initialized
2. ETL pipeline runs for all sources
3. Checkpoints loaded for incremental processing
4. API server starts after ETL completes

### Future Enhancements
Can be extended with:
- Render Cron Jobs (scheduled tasks)
- GitHub Actions (scheduled workflows)
- External schedulers (Airflow, Prefect)

---

## Performance Optimization

### 1. Database
- Indexed columns: `symbol`, `source`, `created_at`
- Connection pooling enabled
- Query optimization with SQLAlchemy

### 2. API
- Response caching (if implemented)
- Pagination for large datasets
- Async/await for concurrent operations

### 3. ETL
- Batch processing for large datasets
- Checkpoint-based resume
- Rate limiting to avoid API throttling

---

## Troubleshooting

### Issue: Container fails to start
**Check:**
1. Render logs for error messages
2. Environment variables are correctly set
3. Database is accessible

**Solution:**
```bash
# View logs
render logs -s kasparro-backend

# Restart service
render restart -s kasparro-backend
```

### Issue: Database connection timeout
**Check:**
1. DATABASE_URL is correct
2. Database service is running
3. Network connectivity

**Solution:** Verify in Render Dashboard → PostgreSQL → Connection Info

### Issue: API returns 5xx errors
**Check:**
1. Application logs
2. Database queries
3. External API status (CoinPaprika, CoinGecko)

---

## Security Measures

### 1. API Security
- ✅ No hardcoded secrets
- ✅ Environment variable based configuration
- ✅ HTTPS only (enforced by Render)
- ✅ Input validation with Pydantic

### 2. Database Security
- ✅ Encrypted connections (SSL)
- ✅ Private network access only
- ✅ Regular backups
- ✅ Parameterized queries (SQL injection prevention)

### 3. Access Control
- Render dashboard requires authentication
- Database credentials stored securely
- API keys rotated regularly

---

## Deployment Timeline

| Date | Event | Status |
|------|-------|--------|
| Dec 27, 2025 | Initial repository created | ✅ |
| Dec 28, 2025 | First deployment to Render | ✅ |
| Dec 29, 2025 | Database configured | ✅ |
| Dec 30, 2025 | ETL pipeline deployed | ✅ |
| Dec 31, 2025 | Documentation updated | ✅ |

---

## Cost Analysis

**Render Free Tier:**
- Web Service: Free with 750 hours/month
- PostgreSQL: Free with 1GB storage
- Bandwidth: 100GB/month

**Production Recommendations:**
- Upgrade to Starter plan for better performance
- Enable auto-scaling for high traffic
- Premium PostgreSQL for larger datasets

---

## Maintenance

### Regular Tasks
- Monitor error rates weekly
- Review logs for anomalies
- Update dependencies monthly
- Rotate API keys quarterly

### Update Procedure
1. Make changes in local environment
2. Test thoroughly with `make test`
3. Commit to feature branch
4. Create pull request
5. Merge to `main` → Auto-deploys

---

## Contact & Support

**For deployment issues:**
- Render Support: https://render.com/docs
- GitHub Issues: https://github.com/pranavraj28/kasparro-backend-pranav-raj/issues

**Maintainer:**
- Name: Pranav Raj
- Email: pranavchoudhary072@gmail.com

---

**Last Updated:** December 31, 2025  
**Next Review:** January 15, 2026

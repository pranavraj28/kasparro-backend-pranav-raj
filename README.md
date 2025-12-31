# Kasparro Backend ETL Assignment - Pranav Raj

## 🌐 Live Cloud Deployment

**Production URL:** https://kasparro-backend-agwk.onrender.com  
**Platform:** Render (Cloud PaaS)  
**Status:** ✅ Live and Operational  
**Deployment Date:** [Add your deployment date, e.g., December 28, 2025]

### 🔍 Quick Verification Endpoints

| Endpoint | URL | Description |
|----------|-----|-------------|
| **Health Check** | [/health](https://kasparro-backend-agwk.onrender.com/health) | System health and DB connectivity |
| **Data API** | [/data](https://kasparro-backend-agwk.onrender.com/data) | Paginated crypto data with filters |
| **Stats** | [/stats](https://kasparro-backend-agwk.onrender.com/stats) | ETL run statistics and metrics |
| **API Docs** | [/docs](https://kasparro-backend-agwk.onrender.com/docs) | Interactive Swagger documentation |

### 🧪 Test Commands
```bash
# Health check
curl https://kasparro-backend-agwk.onrender.com/health

# Get paginated data
curl "https://kasparro-backend-agwk.onrender.com/data?page=1&page_size=10"

# View ETL statistics
curl https://kasparro-backend-agwk.onrender.com/stats

# Filter by source
curl "https://kasparro-backend-agwk.onrender.com/data?source=coinpaprika&page_size=5"
```

---

## 📋 Table of Contents

- [Architecture Overview](#architecture-overview)
- [Features Implemented](#features-implemented)
- [Local Setup](#local-setup)
- [API Documentation](#api-documentation)
- [Data Sources](#data-sources)
- [ETL Pipeline](#etl-pipeline)
- [Testing](#testing)
- [Cloud Deployment](#cloud-deployment)

---

## 🏗️ Architecture Overview
```
┌─────────────────────────────────────────────────────────────┐
│                     Data Sources                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ CoinPaprika  │  │  CoinGecko   │  │  CSV Files   │      │
│  │     API      │  │     API      │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    ETL Pipeline                              │
│  • Incremental ingestion with checkpointing                 │
│  • Data validation (Pydantic schemas)                       │
│  • Normalization & identity unification                     │
│  • Error handling & retry logic                             │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  PostgreSQL Database                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  raw_data    │  │   assets     │  │ checkpoints  │      │
│  │   tables     │  │  (unified)   │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                           │
│  • GET /health   • GET /data   • GET /stats                 │
│  • Pagination    • Filtering   • Metadata                   │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ Features Implemented

### **P0 - Foundation Layer** ✅
- ✅ **P0.1** - Data ingestion from 3 sources (CoinPaprika API, CoinGecko API, CSV)
- ✅ **P0.2** - Backend API with `/data` and `/health` endpoints
- ✅ **P0.3** - Fully Dockerized system with `make` commands
- ✅ **P0.4** - Comprehensive test suite

### **P1 - Growth Layer** ✅
- ✅ **P1.1** - Third data source (CoinGecko API)
- ✅ **P1.2** - Checkpoint-based incremental ingestion
- ✅ **P1.3** - `/stats` endpoint with ETL metadata
- ✅ **P1.4** - Comprehensive test coverage
- ✅ **P1.5** - Clean architecture with separation of concerns

### **P2 - Differentiator Layer** (Partial)
- ✅ **P2.2** - Checkpoint-based recovery on failures
- ✅ **P2.3** - Rate limiting with exponential backoff
- ✅ **P2.4** - Structured logging and observability

---

## 🚀 Local Setup

### Prerequisites
- Docker & Docker Compose
- Make
- Git

### Quick Start
```bash
# Clone the repository
git clone https://github.com/pranavraj28/kasparro-backend-pranav-raj.git
cd kasparro-backend-pranav-raj

# Start the system
make up

# The API will be available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Available Commands
```bash
make up          # Start all services
make down        # Stop all services
make test        # Run test suite
make logs        # View logs
make restart     # Restart services
make clean       # Clean up containers and volumes
```

---

## 📚 API Documentation

### `GET /health`
Returns system health status and database connectivity.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-12-31T12:00:00Z"
}
```

### `GET /data`
Returns paginated cryptocurrency data.

**Query Parameters:**
- `page` (int, default: 1): Page number
- `page_size` (int, default: 20): Items per page
- `source` (string, optional): Filter by data source
- `symbol` (string, optional): Filter by symbol

**Response:**
```json
{
  "data": [...],
  "metadata": {
    "request_id": "uuid",
    "api_latency_ms": 45,
    "page": 1,
    "page_size": 20,
    "total": 500
  }
}
```

### `GET /stats`
Returns ETL statistics and metadata.

**Response:**
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

---

## 🗃️ Data Sources

### 1. CoinPaprika API
- **Type:** REST API
- **Authentication:** API Key
- **Data:** Real-time cryptocurrency market data
- **Rate Limit:** Handled with exponential backoff

### 2. CoinGecko API
- **Type:** REST API
- **Authentication:** Not required
- **Data:** Cryptocurrency pricing and market data
- **Rate Limit:** Implemented

### 3. CSV File
- **Format:** CSV
- **Source:** Local file or uploaded
- **Processing:** Pandas-based parsing

---

## 🔄 ETL Pipeline

### Incremental Ingestion
- Checkpoint-based tracking prevents reprocessing
- Resume from last successful point on failure
- Idempotent writes with upsert logic

### Data Normalization
- Unified schema across all sources
- Identity unification (single canonical coin entity)
- Type validation with Pydantic

### Error Handling
- Retry logic with exponential backoff
- Detailed error logging
- Graceful degradation

---

## 🧪 Testing
```bash
# Run all tests
make test

# Run specific test
pytest tests/test_etl.py

# Run with coverage
pytest --cov=app tests/
```

**Test Coverage:**
- ETL transformation logic
- API endpoints
- Schema validation
- Failure scenarios
- Incremental ingestion

---

## ☁️ Cloud Deployment

### Platform Details
- **Provider:** Render
- **Service Type:** Web Service (Docker)
- **Database:** PostgreSQL (Render managed)
- **Region:** US-East
- **Auto-Deploy:** Enabled from `main` branch

### Deployment Configuration

**Files:**
- `render.yaml` - Render service configuration
- `Dockerfile` - Container build instructions
- `docker-compose.yml` - Local development setup

### Environment Variables
Configured in Render dashboard:
- `DATABASE_URL` - PostgreSQL connection string
- `COINPAPRIKA_API_KEY` - API authentication
- `COINGECKO_API_KEY` - API authentication

### Monitoring
- Health checks every 5 minutes
- Auto-restart on failure
- Logs available in Render dashboard

### ETL Scheduling
ETL runs automatically on container startup. For continuous updates:
- Manual trigger via container restart
- Can be extended with cron jobs or schedulers

---

## 📁 Project Structure
```
kasparro-backend-pranav-raj/
├── app/
│   ├── api/
│   │   └── endpoints.py       # API routes
│   ├── core/
│   │   ├── config.py          # Configuration
│   │   ├── database.py        # DB connection
│   │   └── models.py          # SQLAlchemy models
│   ├── ingestion/
│   │   ├── base.py            # Base ETL logic
│   │   ├── coinpaprika.py     # CoinPaprika ingestion
│   │   ├── coingecko.py       # CoinGecko ingestion
│   │   └── csv_loader.py      # CSV ingestion
│   ├── schemas/
│   │   └── asset.py           # Pydantic schemas
│   └── main.py                # FastAPI app
├── tests/
│   ├── test_api.py
│   ├── test_etl.py
│   └── test_models.py
├── deployment-evidence/       # Deployment screenshots
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── render.yaml
├── requirements.txt
├── DEPLOYMENT.md
└── README.md
```

---

## 👨‍💻 Author

**Pranav Raj**  
Email: pranavchoudhary072@gmail.com  
GitHub: [@pranavraj28](https://github.com/pranavraj28)

---

## 📝 License

This project was created as part of the Kasparro Backend Engineer Intern assignment.

---

## 🙏 Acknowledgments

- Kasparro team for the comprehensive assignment
- CoinPaprika and CoinGecko for API access
- Open-source community for excellent tools

---

**Last Updated:** December 31, 2025

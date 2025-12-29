# Crypto ETL System

A production-ready ETL system for cryptocurrency data ingestion with checkpoint-based recovery, incremental processing, and comprehensive failure handling.

## Architecture Overview

This system is designed with production reliability in mind. It follows a clean architecture pattern that separates concerns into distinct layers:

- **API Layer**: FastAPI endpoints for data access, health checks, and statistics
- **Ingestion Layer**: Pluggable source adapters (CoinPaprika, CoinGecko, CSV)
- **Service Layer**: ETL orchestration with checkpoint management
- **Core Layer**: Database models, configuration, and logging

### Why This Architecture?

1. **Separation of Concerns**: Each layer has a single responsibility, making the codebase maintainable and testable
2. **Extensibility**: New data sources can be added by implementing the `IngestionSource` interface
3. **Resilience**: Checkpoint-based recovery ensures data integrity even during failures
4. **Observability**: Comprehensive logging and health endpoints for monitoring

## Key Features

### ✅ Incremental Ingestion (P0)
- Checkpoint table tracks last processed record per source
- Only processes new data on subsequent runs
- Prevents duplicate processing and reduces API load

### ✅ Failure Recovery (P1)
- Checkpoints are **not updated** on failure, allowing clean resume
- Failed runs can be restarted from the last successful checkpoint
- No data corruption even if ETL crashes mid-run

### ✅ Production-Ready APIs
- `/data` - Paginated, filterable asset data with request metadata
- `/health` - Database connectivity and ETL status
- `/stats` - ETL run statistics and metrics

### ✅ Failure Injection Testing (P2)
- Environment variable `FAIL_AFTER_N_RECORDS` for controlled failure testing
- Demonstrates recovery capabilities in real scenarios

## Data Model

### Raw Tables
Store complete payloads from each source for auditability and reprocessing:
- `raw_coinpaprika` - Full CoinPaprika API responses
- `raw_coingecko` - Full CoinGecko API responses  
- `raw_csv_source` - CSV file records

### Unified Table
Normalized asset data across all sources:
```sql
assets (
  asset_id,
  symbol,
  name,
  price_usd,
  market_cap,
  source,
  updated_at
)
```

### Checkpoint Table
Tracks ETL progress for recovery:
```sql
etl_checkpoints (
  source,
  last_processed_id,
  last_processed_at,
  status,
  run_id
)
```

## How Incremental Ingestion Works

1. **First Run**: No checkpoint exists, processes all available data
2. **Subsequent Runs**: 
   - Reads `last_processed_id` from checkpoint
   - Fetches only records after that ID (source-dependent)
   - Updates checkpoint only after successful batch processing
3. **On Failure**: Checkpoint remains at last successful point, allowing resume

## How Recovery Works

The checkpoint system ensures atomic progress tracking:

1. **Start Run**: Checkpoint status set to "running", new `run_id` generated
2. **Process Batch**: 
   - Save raw data → get ID
   - Normalize and save to unified table
   - **Only then** update checkpoint with new `last_processed_id`
3. **On Success**: Status set to "completed"
4. **On Failure**: Status set to "failed", but `last_processed_id` is **NOT rolled back**

This means:
- ✅ Partial progress is preserved
- ✅ Resume starts from last successful batch
- ✅ No duplicate processing
- ✅ No data loss

## Local Development

### Prerequisites
- Docker and Docker Compose
- Make (optional, but recommended)

### Quick Start

```bash
# Start all services
make up

# Or manually:
docker-compose up -d

# Run tests
make test

# View logs
make logs

# Stop services
make down
```

The API will be available at `http://localhost:8000`

### Manual Setup (Without Docker)

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database (PostgreSQL required)
export DATABASE_URL="postgresql://user:pass@localhost:5432/crypto_etl"

# Run migrations
alembic upgrade head

# Start API
uvicorn app.main:app --reload
```

## Testing Failure Recovery

The system includes failure injection for testing recovery:

```bash
# Set environment variable
export FAIL_AFTER_N_RECORDS=10

# Start ETL - it will fail after processing 10 records
docker-compose up

# Check checkpoint (should show last_processed_id=10, status=failed)
curl http://localhost:8000/stats

# Remove failure injection and restart
unset FAIL_AFTER_N_RECORDS
docker-compose restart api

# ETL will resume from record 11
```

## API Endpoints

### GET /data
Retrieve paginated asset data with filtering.

**Query Parameters:**
- `page` (int): Page number (default: 1)
- `page_size` (int): Records per page (default: 50, max: 100)
- `symbol` (string, optional): Filter by symbol (case-insensitive partial match)
- `source` (string, optional): Filter by source name

**Response:**
```json
{
  "request_id": "uuid",
  "api_latency_ms": 42.5,
  "data": [...],
  "total": 150,
  "page": 1,
  "page_size": 50
}
```

### GET /health
Health check with database and ETL status.

**Response:**
```json
{
  "status": "healthy",
  "database": "healthy",
  "etl": "healthy",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### GET /stats
ETL statistics and run information.

**Response:**
```json
{
  "records_processed": 1000,
  "last_success": "2024-01-01T12:00:00",
  "last_failure": null,
  "sources": {
    "coinpaprika": {
      "last_processed_id": 500,
      "last_processed_at": "2024-01-01T12:00:00",
      "status": "completed",
      "run_id": "uuid"
    }
  }
}
```

## Deployment

> **⚠️ IMPORTANT**: Cloud deployment is required for submission. See `DEPLOYMENT_GUIDE.md` for detailed instructions.

### Quick Deployment Options

1. **AWS EC2** - See `DEPLOYMENT_GUIDE.md` for step-by-step instructions
2. **GCP Compute Engine** - See `DEPLOYMENT_GUIDE.md` for step-by-step instructions  
3. **Azure VM** - See `DEPLOYMENT_GUIDE.md` for step-by-step instructions

### AWS EC2 Deployment

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t3.medium or larger
   - Security group: Allow ports 22 (SSH), 8000 (API)

2. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install -y docker.io docker-compose make
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

3. **Deploy Application**
   ```bash
   git clone <repository>
   cd kasparro-etl-assignment
   cp .env.example .env
   # Edit .env with production values
   make up
   ```

4. **Set Up Cron (Alternative to Background Task)**
   ```bash
   crontab -e
   # Add: */5 * * * * cd /path/to/app && docker-compose exec -T api python -m app.services.etl_runner
   ```

5. **Set Up Logging (CloudWatch)**
   ```bash
   # Install CloudWatch agent
   wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
   sudo dpkg -i amazon-cloudwatch-agent.deb
   # Configure to ship Docker logs
   ```

6. **Nginx Reverse Proxy (Optional)**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Environment Variables

Key production settings:
```bash
DATABASE_URL=postgresql://user:pass@db-host:5432/crypto_etl
ETL_INTERVAL_SECONDS=300
LOG_LEVEL=INFO
COINPAPRIKA_API_KEY=your_key_here  # Optional
COINGECKO_API_KEY=your_key_here    # Optional
```

## Project Structure

```
app/
 ├── api/              # FastAPI routes
 │    ├── routes.py    # /data endpoint
 │    ├── health.py    # /health endpoint
 │    └── stats.py     # /stats endpoint
 ├── ingestion/        # Data source adapters
 │    ├── base.py      # Abstract base class
 │    ├── coinpaprika.py
 │    ├── coingecko.py
 │    └── csv_source.py
 ├── services/         # Business logic
 │    ├── etl_runner.py    # Main ETL orchestration
 │    └── checkpoint.py    # Checkpoint management
 ├── schemas/          # Pydantic models
 │    ├── unified.py   # Unified asset schema
 │    └── raw.py       # Raw data schemas
 └── core/             # Core infrastructure
      ├── config.py    # Settings
      ├── db.py        # Database connection
      ├── models.py    # SQLAlchemy models
      └── logging.py   # Logging setup
tests/                 # Test suite
Dockerfile
docker-compose.yml
Makefile
README.md
```

## Design Decisions

### Why PostgreSQL?
- ACID compliance for data integrity
- JSONB support for flexible raw data storage
- Mature ecosystem with excellent Python support

### Why Checkpoint Table vs. File-Based?
- Database-backed checkpoints are transactional
- Can be queried via API for observability
- Survives container restarts
- Enables distributed ETL in future

### Why Batch Processing?
- Reduces memory usage for large datasets
- Allows progress tracking at batch level
- Enables partial recovery (resume from last successful batch)

### Why Separate Raw and Unified Tables?
- **Auditability**: Full source data preserved
- **Reprocessing**: Can re-run normalization logic without re-fetching
- **Debugging**: Inspect raw payloads when normalization fails
- **Compliance**: Historical record of what was received

## Testing

Run the test suite:
```bash
make test
```

Test coverage includes:
- ✅ ETL transforms valid data correctly
- ✅ Duplicate ingestion does not re-insert
- ✅ Failure mid-ETL → resume works
- ✅ /health returns DB + ETL status
- ✅ /data pagination works
- ✅ Failure injection and recovery

## Monitoring

The system exposes several observability endpoints:

- `/health` - Quick health check for load balancers
- `/stats` - Detailed ETL metrics
- Application logs - Structured logging to stdout

For production, consider:
- Prometheus metrics endpoint (future enhancement)
- CloudWatch/DataDog integration
- Alerting on failed ETL runs

## Future Enhancements

- [ ] Rate limiting on API endpoints
- [ ] Authentication/authorization
- [ ] WebSocket support for real-time updates
- [ ] Additional data sources (Binance, Kraken, etc.)
- [ ] Data quality validation rules
- [ ] Automated schema evolution handling

## License

MIT

## Author

Built for Kasparro backend engineering assessment.


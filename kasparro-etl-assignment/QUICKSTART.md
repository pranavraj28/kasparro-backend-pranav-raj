# Quick Start Guide

Get the system running in 3 commands:

```bash
# 1. Start everything
make up

# 2. Verify it's working
curl http://localhost:8000/health

# 3. Check the API docs
open http://localhost:8000/docs
```

## Test the ETL

The ETL runs automatically every 5 minutes. To trigger manually:

```bash
# View logs to see ETL running
make logs

# Or check stats
curl http://localhost:8000/stats
```

## Test Failure Recovery

```bash
# Set failure injection
export FAIL_AFTER_N_RECORDS=5

# Restart API (will fail after 5 records)
docker-compose restart api

# Check checkpoint (should show failed status)
curl http://localhost:8000/stats

# Remove failure injection and restart (will resume)
unset FAIL_AFTER_N_RECORDS
docker-compose restart api
```

## Run Tests

```bash
make test
```

## Access Data

```bash
# Get all assets
curl http://localhost:8000/data

# Filter by symbol
curl "http://localhost:8000/data?symbol=BTC"

# Filter by source
curl "http://localhost:8000/data?source=coinpaprika"

# Pagination
curl "http://localhost:8000/data?page=1&page_size=10"
```

That's it! 🚀


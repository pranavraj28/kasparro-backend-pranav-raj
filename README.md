Kasparro Backend & ETL Assignment
This repository contains my submission for the Kasparro Backend Engineer Internship Assignment.
It implements a production-ready ETL pipeline with canonical asset normalization, persistent storage, and a public API.

🚀 Live Public Cloud Deployment (Verified)
The system is live, publicly deployed, and verifiable.

🔗 Deployed Backend URL (Render)
👉 https://kasparro-backend-agwk.onrender.com

✅ Verification Endpoints
Health / Root
https://kasparro-backend-agwk.onrender.com/

Unified Canonical Data API
https://kasparro-backend-agwk.onrender.com/data

Swagger API Documentation
https://kasparro-backend-agwk.onrender.com/docs

This deployment satisfies the public cloud deployment requirement of the assignment and can be verified without any local setup.

📌 Assignment Scope Covered
✔ Public cloud deployment (Render)
✔ Dockerized backend
✔ Executable ETL system
✔ Canonical asset normalization across multiple sources
✔ Checkpoint-based ingestion
✔ Verifiable API output
✔ No hardcoded secrets
✔ Real data sources (CoinPaprika, CoinGecko)

🧠 System Overview
The system ingests cryptocurrency market data from multiple sources, normalizes assets into canonical coins, and exposes unified results through a REST API.

Data Sources
CoinPaprika API

CoinGecko API

Key Features
Canonical coin unification (e.g., BTC across sources)

Source-to-canonical mapping

Latest price selection per asset

Idempotent ETL runs

Docker-based execution

Public API for consumption

🗂 Project Structure
kasparro-etl/
├── app/
│   ├── api/
│   │   ├── main.py              # FastAPI app entrypoint
│   │   └── routes/
│   │       └── data.py           # /data endpoint
│   ├── core/
│   │   ├── database/             # DB session & initialization
│   │   ├── logging/              # Centralized logging
│   │   └── models.py             # SQLAlchemy models
│   ├── ingestion/
│   │   ├── base.py               # Ingestion base class
│   │   ├── coinpaprika.py
│   │   ├── coingecko.py
│   │   └── normalize.py          # Canonical normalization logic
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run_etl.py                    # ETL execution entrypoint
└── README.md
🔁 ETL & Normalization Logic
Canonical Coin Model
Each coin exists once in the system

Multiple sources map to a single canonical coin

Prices are always stored against the canonical entity

Normalization Flow
Fetch raw data from source

Normalize symbol (e.g., aliases → canonical symbol)

Create or reuse canonical coin

Store source mapping

Insert latest price snapshot

This prevents duplication and ensures clean downstream consumption.

🌐 API Details
GET /data
Returns unified canonical coins with all available sources and latest price.

Example Response

[
  {
    "symbol": "BTC",
    "name": "Bitcoin",
    "sources": ["coingecko", "coinpaprika"],
    "latest_price_usd": 87593.11
  }
]
🐳 Docker & Execution
Run Locally (Optional)
docker compose up --build
Run ETL Manually
docker compose exec api python run_etl.py
🔐 Secrets & Configuration
No secrets are hardcoded

API keys are optional

System works without paid API access

Production deployment uses environment-based configuration

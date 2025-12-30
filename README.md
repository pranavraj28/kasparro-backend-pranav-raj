# Kasparro ETL Backend — Crypto Asset Data API

This repository contains a production-ready backend service that ingests, normalizes, and serves cryptocurrency asset data from multiple sources. It is part of the Kasparro backend assignment and exposes a unified API for querying canonical asset data.

---

## 🚀 Live Deployment

🔗 **API Base URL:**  
https://kasparro-backend-agwk.onrender.com

🔗 **Swagger / OpenAPI Docs:**  
https://kasparro-backend-agwk.onrender.com/docs

---

## 📦 Overview

This project implements:

- **Incremental ETL pipelines** for multiple data sources
  - CoinPaprika
  - CoinGecko (rate-limited but gracefully handled)
  - CSV (if configured)
- **Canonical data model**
  - Avoids duplicate assets across sources
  - Stored in SQLite (or configured RDBMS)
- **REST API Endpoints**
  - `/data` — Paginated unified asset data
  - `/health` — Health check with ETL and DB status
  - `/stats` — ETL run and ingestion statistics

---

## 📌 Core Features

### ✅ Normalized Canonical Assets

The API returns a unified view of assets with canonical identity, ensuring that the same asset (e.g. BTC) appears once regardless of source.

Example output:

```json
[
  {
    "symbol": "BTC",
    "name": "Bitcoin",
    "sources": ["coinpaprika", "coingecko"],
    "latest_price_usd": 87593.11
  }
]

## 🚀 Live Public Cloud Deployment (Verified)

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



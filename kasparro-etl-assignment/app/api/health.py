"""Health check endpoint."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from app.core.db import get_db
from app.services.etl_runner import ETLRunner
from app.core.logging import logger

router = APIRouter()


@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint with DB connectivity and ETL status."""
    try:
        # Check DB connectivity
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"
        raise HTTPException(status_code=503, detail="Database connection failed")
    
    # Get ETL status
    try:
        etl_runner = ETLRunner(db)
        etl_stats = etl_runner.get_stats()
        
        # Determine overall ETL status
        etl_status = "healthy"
        for source_stats in etl_stats.values():
            if source_stats["status"] == "failed":
                etl_status = "degraded"
                break
        
    except Exception as e:
        logger.error(f"ETL status check failed: {e}")
        etl_status = "unknown"
    
    return {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "database": db_status,
        "etl": etl_status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


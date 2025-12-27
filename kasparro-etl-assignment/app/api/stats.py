"""ETL statistics endpoint."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.services.etl_runner import ETLRunner
from app.core.models import ETLCheckpoint
from sqlalchemy import func

router = APIRouter()


@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get ETL statistics."""
    etl_runner = ETLRunner(db)
    checkpoint_stats = etl_runner.get_stats()
    
    # Aggregate stats
    all_checkpoints = db.query(ETLCheckpoint).all()
    
    # Get last success and failure times
    last_success = None
    last_failure = None
    
    for checkpoint in all_checkpoints:
        if checkpoint.status == "completed" and checkpoint.last_processed_at:
            if not last_success or checkpoint.last_processed_at > last_success:
                last_success = checkpoint.last_processed_at
        elif checkpoint.status == "failed" and checkpoint.updated_at:
            if not last_failure or checkpoint.updated_at > last_failure:
                last_failure = checkpoint.updated_at
    
    # Count total records processed (approximate from checkpoints)
    total_records = sum(
        stats.get("last_processed_id", 0) or 0
        for stats in checkpoint_stats.values()
    )
    
    return {
        "records_processed": total_records,
        "last_success": last_success.isoformat() if last_success else None,
        "last_failure": last_failure.isoformat() if last_failure else None,
        "sources": checkpoint_stats,
    }


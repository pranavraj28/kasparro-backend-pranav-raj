"""Checkpoint management for ETL recovery."""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import uuid
from app.core.models import ETLCheckpoint
from app.core.logging import logger


class CheckpointService:
    """Service for managing ETL checkpoints."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_checkpoint(self, source: str) -> ETLCheckpoint:
        """Get or create checkpoint for a source."""
        checkpoint = self.db.query(ETLCheckpoint).filter(
            ETLCheckpoint.source == source
        ).first()
        
        if not checkpoint:
            checkpoint = ETLCheckpoint(
                source=source,
                status="pending",
                run_id=str(uuid.uuid4())
            )
            self.db.add(checkpoint)
            self.db.commit()
            self.db.refresh(checkpoint)
        
        return checkpoint
    
    def start_run(self, source: str) -> str:
        """Start a new ETL run. Returns run_id."""
        checkpoint = self.get_checkpoint(source)
        checkpoint.status = "running"
        checkpoint.run_id = str(uuid.uuid4())
        checkpoint.updated_at = datetime.utcnow()
        self.db.commit()
        return checkpoint.run_id
    
    def update_progress(self, source: str, last_processed_id: int):
        """Update checkpoint with progress. Only called on successful batch processing."""
        checkpoint = self.get_checkpoint(source)
        checkpoint.last_processed_id = last_processed_id
        checkpoint.last_processed_at = datetime.utcnow()
        # Don't update status here - only on completion or failure
        self.db.commit()
    
    def complete_run(self, source: str):
        """Mark ETL run as completed."""
        checkpoint = self.get_checkpoint(source)
        checkpoint.status = "completed"
        checkpoint.updated_at = datetime.utcnow()
        self.db.commit()
        logger.info(f"ETL run completed for {source}")
    
    def fail_run(self, source: str, error: str = None):
        """Mark ETL run as failed. Checkpoint is NOT updated, allowing resume."""
        checkpoint = self.get_checkpoint(source)
        checkpoint.status = "failed"
        checkpoint.updated_at = datetime.utcnow()
        self.db.commit()
        logger.error(f"ETL run failed for {source}: {error}")
    
    def get_last_processed_id(self, source: str) -> int:
        """Get the last processed ID for a source."""
        checkpoint = self.get_checkpoint(source)
        return checkpoint.last_processed_id if checkpoint else None


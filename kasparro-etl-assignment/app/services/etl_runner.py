"""ETL runner with checkpoint-based recovery."""
import time
from datetime import datetime
from sqlalchemy.orm import Session
from app.ingestion.base import IngestionSource
from app.ingestion.coinpaprika import CoinPaprikaSource
from app.ingestion.coingecko import CoinGeckoSource
from app.ingestion.csv_source import CSVSource
from app.services.checkpoint import CheckpointService
from app.core.logging import logger
from app.core.config import settings


class ETLRunner:
    """Main ETL runner with failure recovery."""
    
    def __init__(self, db: Session):
        self.db = db
        self.checkpoint_service = CheckpointService(db)
        self.sources: dict[str, IngestionSource] = {
            "coinpaprika": CoinPaprikaSource(db),
            "coingecko": CoinGeckoSource(db),
            "csv_source": CSVSource(db),
        }
    
    def run_source(self, source_name: str) -> dict:
        """Run ETL for a single source with checkpoint recovery."""
        start_time = time.time()
        records_processed = 0
        run_id = None
        
        try:
            # Start run and get checkpoint
            run_id = self.checkpoint_service.start_run(source_name)
            last_processed_id = self.checkpoint_service.get_last_processed_id(source_name)
            
            logger.info(f"Starting ETL for {source_name} (resuming from ID: {last_processed_id})")
            
            source = self.sources[source_name]
            
            # Fetch data
            raw_data = source.fetch_data(last_processed_id)
            if not raw_data:
                logger.warning(f"No data fetched from {source_name}")
                self.checkpoint_service.complete_run(source_name)
                return {
                    "source": source_name,
                    "status": "completed",
                    "records_processed": 0,
                    "duration": time.time() - start_time,
                    "run_id": run_id,
                }
            
            # Process in batches
            batch_size = settings.ETL_BATCH_SIZE
            total_records = len(raw_data)
            
            for i in range(0, total_records, batch_size):
                batch = raw_data[i:i + batch_size]
                
                # Save raw data first
                batch_ids = []
                for record in batch:
                    raw_id = source.save_raw(record)
                    batch_ids.append(raw_id)
                
                # Process batch
                processed = source.process_batch(batch)
                records_processed += processed
                
                # Update checkpoint after successful batch
                last_id = batch_ids[-1] if batch_ids else None
                if last_id:
                    self.checkpoint_service.update_progress(source_name, last_id)
                
                # Failure injection for testing
                if settings.FAIL_AFTER_N_RECORDS is not None and records_processed >= settings.FAIL_AFTER_N_RECORDS:
                    raise Exception(f"Failure injection triggered after {records_processed} records")
                
                logger.info(f"Processed batch {i//batch_size + 1} for {source_name}: {processed} records")
            
            # Mark as completed
            self.checkpoint_service.complete_run(source_name)
            
            duration = time.time() - start_time
            logger.info(f"ETL completed for {source_name}: {records_processed} records in {duration:.2f}s")
            
            return {
                "source": source_name,
                "status": "completed",
                "records_processed": records_processed,
                "duration": duration,
                "run_id": run_id,
            }
            
        except Exception as e:
            # Mark as failed but don't update checkpoint - allows resume
            self.checkpoint_service.fail_run(source_name, str(e))
            duration = time.time() - start_time
            
            logger.error(f"ETL failed for {source_name} after {duration:.2f}s: {e}", exc_info=True)
            
            return {
                "source": source_name,
                "status": "failed",
                "records_processed": records_processed,
                "duration": duration,
                "error": str(e),
                "run_id": run_id,
            }
    
    def run_all(self) -> dict:
        """Run ETL for all sources."""
        results = {}
        overall_start = time.time()
        
        for source_name in self.sources.keys():
            results[source_name] = self.run_source(source_name)
        
        return {
            "overall_duration": time.time() - overall_start,
            "sources": results,
            "timestamp": datetime.utcnow().isoformat(),
        }
    
    def get_stats(self) -> dict:
        """Get ETL statistics from checkpoints."""
        stats = {}
        
        for source_name in self.sources.keys():
            checkpoint = self.checkpoint_service.get_checkpoint(source_name)
            stats[source_name] = {
                "last_processed_id": checkpoint.last_processed_id,
                "last_processed_at": checkpoint.last_processed_at.isoformat() if checkpoint.last_processed_at else None,
                "status": checkpoint.status,
                "run_id": checkpoint.run_id,
            }
        
        return stats


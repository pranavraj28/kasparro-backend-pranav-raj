"""Base class for data ingestion sources."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.core.logging import logger


class IngestionSource(ABC):
    """Abstract base class for all ingestion sources."""
    
    def __init__(self, source_name: str, db: Session):
        self.source_name = source_name
        self.db = db
    
    @abstractmethod
    def fetch_data(self, last_processed_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Fetch raw data from the source."""
        pass
    
    @abstractmethod
    def normalize(self, raw_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Normalize raw data to unified asset format."""
        pass
    
    def save_raw(self, payload: Dict[str, Any]) -> int:
        """Save raw data to the appropriate raw table. Returns the inserted ID."""
        raise NotImplementedError("Subclasses must implement save_raw")
    
    def process_batch(self, batch: List[Dict[str, Any]]) -> int:
        """Process a batch of raw data records."""
        processed = 0
        for record in batch:
            try:
                normalized = self.normalize(record)
                if normalized:
                    self.save_unified(normalized)
                    processed += 1
                else:
                    logger.warning(f"Failed to normalize record from {self.source_name}: {record.get('id', 'unknown')}")
            except Exception as e:
                logger.error(f"Error processing record from {self.source_name}: {e}", exc_info=True)
        return processed
    
    def save_unified(self, asset_data: Dict[str, Any]):
        """Save normalized data to unified assets table."""
        from app.core.models import Asset
        
        # Use upsert logic: update if exists, insert if not
        existing = self.db.query(Asset).filter(
            Asset.symbol == asset_data['symbol'],
            Asset.source == asset_data['source']
        ).first()
        
        if existing:
            existing.name = asset_data['name']
            existing.price_usd = asset_data.get('price_usd')
            existing.market_cap = asset_data.get('market_cap')
        else:
            new_asset = Asset(**asset_data)
            self.db.add(new_asset)
        
        self.db.commit()


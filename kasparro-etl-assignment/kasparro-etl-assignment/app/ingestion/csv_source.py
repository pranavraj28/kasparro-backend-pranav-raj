"""CSV file ingestion source."""
import csv
import os
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.ingestion.base import IngestionSource
from app.core.models import RawCSVSource
from app.core.logging import logger
from app.core.config import settings


class CSVSource(IngestionSource):
    """Ingestion source for CSV files."""
    
    def __init__(self, db: Session, csv_path: Optional[str] = None):
        super().__init__("csv_source", db)
        self.csv_path = csv_path or settings.CSV_SOURCE_PATH or "data/sample.csv"
    
    def fetch_data(self, last_processed_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Read data from CSV file."""
        try:
            if not os.path.exists(self.csv_path):
                logger.warning(f"CSV file not found: {self.csv_path}")
                return []
            
            records = []
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for idx, row in enumerate(reader, start=1):
                    # Skip if we have a checkpoint and this is before it
                    if last_processed_id is not None and idx <= last_processed_id:
                        continue
                    records.append(row)
            
            return records
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}", exc_info=True)
            return []
    
    def normalize(self, raw_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Normalize CSV data to unified format."""
        try:
            # CSV format may vary, try common field names
            symbol = raw_data.get("symbol") or raw_data.get("Symbol") or raw_data.get("SYMBOL", "")
            name = raw_data.get("name") or raw_data.get("Name") or raw_data.get("NAME", "")
            
            # Try to parse price and market cap
            price_usd = None
            market_cap = None
            
            for price_key in ["price", "Price", "PRICE", "price_usd", "priceUSD"]:
                if price_key in raw_data:
                    try:
                        price_usd = float(raw_data[price_key])
                        break
                    except (ValueError, TypeError):
                        continue
            
            for cap_key in ["market_cap", "MarketCap", "MARKET_CAP", "marketCap"]:
                if cap_key in raw_data:
                    try:
                        market_cap = float(raw_data[cap_key])
                        break
                    except (ValueError, TypeError):
                        continue
            
            return {
                "symbol": str(symbol).upper(),
                "name": str(name),
                "price_usd": price_usd,
                "market_cap": market_cap,
                "source": self.source_name,
            }
        except Exception as e:
            logger.error(f"Error normalizing CSV data: {e}", exc_info=True)
            return None
    
    def save_raw(self, payload: Dict[str, Any]) -> int:
        """Save raw CSV data."""
        raw_record = RawCSVSource(
            source_name=self.source_name,
            payload=payload,
            fetched_at=datetime.utcnow()
        )
        self.db.add(raw_record)
        self.db.commit()
        self.db.refresh(raw_record)
        return raw_record.id


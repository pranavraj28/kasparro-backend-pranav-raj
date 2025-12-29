"""CoinPaprika API ingestion source."""
import httpx
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.ingestion.base import IngestionSource
from app.core.models import RawCoinPaprika
from app.core.logging import logger
from app.core.config import settings


class CoinPaprikaSource(IngestionSource):
    """Ingestion source for CoinPaprika API."""
    
    BASE_URL = "https://api.coinpaprika.com/v1"
    
    def __init__(self, db: Session):
        super().__init__("coinpaprika", db)
        self.api_key = settings.COINPAPRIKA_API_KEY
    
    def fetch_data(self, last_processed_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Fetch ticker data from CoinPaprika."""
        try:
            url = f"{self.BASE_URL}/tickers"
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            with httpx.Client(timeout=30.0) as client:
                response = client.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                
                # Filter if we have a checkpoint
                if last_processed_id is not None:
                    # CoinPaprika doesn't have incremental IDs, so we'll process all
                    # but track by timestamp or process in batches
                    pass
                
                return data if isinstance(data, list) else []
        except Exception as e:
            logger.error(f"Error fetching from CoinPaprika: {e}", exc_info=True)
            return []
    
    def normalize(self, raw_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Normalize CoinPaprika data to unified format."""
        try:
            return {
                "symbol": raw_data.get("symbol", "").upper(),
                "name": raw_data.get("name", ""),
                "price_usd": raw_data.get("quotes", {}).get("USD", {}).get("price"),
                "market_cap": raw_data.get("quotes", {}).get("USD", {}).get("market_cap"),
                "source": self.source_name,
            }
        except Exception as e:
            logger.error(f"Error normalizing CoinPaprika data: {e}", exc_info=True)
            return None
    
    def save_raw(self, payload: Dict[str, Any]) -> int:
        """Save raw CoinPaprika data."""
        raw_record = RawCoinPaprika(
            source_name=self.source_name,
            payload=payload,
            fetched_at=datetime.utcnow()
        )
        self.db.add(raw_record)
        self.db.commit()
        self.db.refresh(raw_record)
        return raw_record.id


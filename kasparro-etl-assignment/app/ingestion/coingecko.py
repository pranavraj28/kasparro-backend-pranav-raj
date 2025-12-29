"""CoinGecko API ingestion source."""
import httpx
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime
from app.ingestion.base import IngestionSource
from app.core.models import RawCoinGecko
from app.core.logging import logger
from app.core.config import settings


class CoinGeckoSource(IngestionSource):
    """Ingestion source for CoinGecko API."""
    
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    def __init__(self, db: Session):
        super().__init__("coingecko", db)
        self.api_key = settings.COINGECKO_API_KEY
    
    def fetch_data(self, last_processed_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Fetch market data from CoinGecko."""
        try:
            url = f"{self.BASE_URL}/coins/markets"
            params = {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 250,
                "page": 1,
            }
            headers = {}
            if self.api_key:
                headers["x-cg-demo-api-key"] = self.api_key
            
            with httpx.Client(timeout=30.0) as client:
                response = client.get(url, params=params, headers=headers)
                response.raise_for_status()
                data = response.json()
                
                return data if isinstance(data, list) else []
        except Exception as e:
            logger.error(f"Error fetching from CoinGecko: {e}", exc_info=True)
            return []
    
    def normalize(self, raw_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Normalize CoinGecko data to unified format."""
        try:
            return {
                "symbol": raw_data.get("symbol", "").upper(),
                "name": raw_data.get("name", ""),
                "price_usd": raw_data.get("current_price"),
                "market_cap": raw_data.get("market_cap"),
                "source": self.source_name,
            }
        except Exception as e:
            logger.error(f"Error normalizing CoinGecko data: {e}", exc_info=True)
            return None
    
    def save_raw(self, payload: Dict[str, Any]) -> int:
        """Save raw CoinGecko data."""
        raw_record = RawCoinGecko(
            source_name=self.source_name,
            payload=payload,
            fetched_at=datetime.utcnow()
        )
        self.db.add(raw_record)
        self.db.commit()
        self.db.refresh(raw_record)
        return raw_record.id


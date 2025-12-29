"""Pydantic schemas for raw data ingestion."""
from pydantic import BaseModel
from typing import Any, Dict
from datetime import datetime


class RawDataBase(BaseModel):
    """Base schema for raw data."""
    source_name: str
    payload: Dict[str, Any]
    fetched_at: datetime


class RawCoinPaprikaCreate(RawDataBase):
    """Schema for creating raw CoinPaprika data."""
    pass


class RawCoinGeckoCreate(RawDataBase):
    """Schema for creating raw CoinGecko data."""
    pass


class RawCSVSourceCreate(RawDataBase):
    """Schema for creating raw CSV source data."""
    pass


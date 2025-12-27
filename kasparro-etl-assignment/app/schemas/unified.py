"""Pydantic schemas for unified asset data."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AssetBase(BaseModel):
    """Base schema for unified asset."""
    symbol: str
    name: str
    price_usd: Optional[float] = None
    market_cap: Optional[float] = None
    source: str


class AssetCreate(AssetBase):
    """Schema for creating an asset."""
    pass


class AssetResponse(AssetBase):
    """Schema for asset API response."""
    asset_id: int
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class AssetListResponse(BaseModel):
    """Schema for paginated asset list response."""
    request_id: str
    api_latency_ms: float
    data: list[AssetResponse]
    total: int
    page: int
    page_size: int


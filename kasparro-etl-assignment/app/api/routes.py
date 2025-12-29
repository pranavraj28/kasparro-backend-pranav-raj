"""Main API routes."""
import time
import uuid
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.core.db import get_db
from app.core.models import Asset
from app.schemas.unified import AssetListResponse, AssetResponse
from app.core.logging import logger

router = APIRouter()


@router.get("/data", response_model=AssetListResponse)
async def get_data(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    symbol: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Get paginated asset data with filtering."""
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    try:
        # Build query
        query = db.query(Asset)
        
        if symbol:
            query = query.filter(Asset.symbol.ilike(f"%{symbol}%"))
        
        if source:
            query = query.filter(Asset.source == source)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * page_size
        assets = query.order_by(Asset.updated_at.desc()).offset(offset).limit(page_size).all()
        
        # Convert to response models
        asset_responses = [AssetResponse.model_validate(asset) for asset in assets]
        
        api_latency_ms = (time.time() - start_time) * 1000
        
        return AssetListResponse(
            request_id=request_id,
            api_latency_ms=api_latency_ms,
            data=asset_responses,
            total=total,
            page=page,
            page_size=page_size,
        )
    except Exception as e:
        logger.error(f"Error fetching data: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


"""SQLAlchemy database models."""
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Text, Index
from sqlalchemy.sql import func
from app.core.db import Base


class RawCoinPaprika(Base):
    """Raw data from CoinPaprika API."""
    __tablename__ = "raw_coinpaprika"
    
    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String, default="coinpaprika", nullable=False)
    payload = Column(JSON, nullable=False)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    __table_args__ = (
        Index('idx_coinpaprika_fetched', 'fetched_at'),
    )


class RawCoinGecko(Base):
    """Raw data from CoinGecko API."""
    __tablename__ = "raw_coingecko"
    
    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String, default="coingecko", nullable=False)
    payload = Column(JSON, nullable=False)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    __table_args__ = (
        Index('idx_coingecko_fetched', 'fetched_at'),
    )


class RawCSVSource(Base):
    """Raw data from CSV source."""
    __tablename__ = "raw_csv_source"
    
    id = Column(Integer, primary_key=True, index=True)
    source_name = Column(String, default="csv_source", nullable=False)
    payload = Column(JSON, nullable=False)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    __table_args__ = (
        Index('idx_csv_fetched', 'fetched_at'),
    )


class Asset(Base):
    """Unified asset table with normalized data."""
    __tablename__ = "assets"
    
    asset_id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    price_usd = Column(Float, nullable=True)
    market_cap = Column(Float, nullable=True)
    source = Column(String, nullable=False, index=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    __table_args__ = (
        Index('idx_assets_symbol_source', 'symbol', 'source', unique=True),
        Index('idx_assets_updated', 'updated_at'),
    )


class ETLCheckpoint(Base):
    """ETL checkpoint table for incremental ingestion and recovery."""
    __tablename__ = "etl_checkpoints"
    
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False, unique=True, index=True)
    last_processed_id = Column(Integer, nullable=True)
    last_processed_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, nullable=False, default="pending")  # pending, running, completed, failed
    run_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


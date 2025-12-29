from sqlalchemy.orm import Session
from app.core.models import Coin, CoinSourceMapping, AssetPrice
from datetime import datetime
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class CoinNormalizationService:
    """
    Handles the unification of coins across multiple data sources.
    This is the KEY service that fixes the -20 point deduction.
    """
    
    # Symbol normalization rules (handle inconsistencies across sources)
    SYMBOL_ALIASES = {
        'BTC': ['BITCOIN', 'XBT'],
        'ETH': ['ETHEREUM'],
        'USDT': ['TETHER'],
        # Add more as needed
    }
    
    @staticmethod
    def normalize_symbol(symbol: str) -> str:
        """Normalize symbol to canonical form"""
        symbol = symbol.upper().strip()
        
        # Check if this is an alias
        for canonical, aliases in CoinNormalizationService.SYMBOL_ALIASES.items():
            if symbol in aliases:
                return canonical
        
        return symbol
    
    @staticmethod
    def get_or_create_coin(
        db: Session,
        symbol: str,
        name: str,
        source: str,
        source_id: str,
        source_symbol: Optional[str] = None,
        source_name: Optional[str] = None
    ) -> Coin:
        """
        Get existing canonical coin or create new one.
        Also creates/updates the source mapping.
        
        This is the CORE normalization logic:
        1. Normalize the symbol
        2. Find or create canonical coin
        3. Link source-specific data to canonical coin
        """
        
        # Step 1: Normalize symbol
        normalized_symbol = CoinNormalizationService.normalize_symbol(symbol)
        
        # Step 2: Check if we already have a source mapping for this source_id
        existing_mapping = db.query(CoinSourceMapping).filter(
            CoinSourceMapping.source == source,
            CoinSourceMapping.source_id == source_id
        ).first()
        
        if existing_mapping:
            # Update last seen
            existing_mapping.last_seen = datetime.utcnow()
            db.commit()
            return existing_mapping.coin
        
        # Step 3: Look for canonical coin by symbol
        canonical_coin = db.query(Coin).filter(
            Coin.symbol == normalized_symbol
        ).first()
        
        if not canonical_coin:
            # Create new canonical coin
            canonical_coin = Coin(
                symbol=normalized_symbol,
                name=name,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(canonical_coin)
            db.flush()  # Get the ID without committing
            logger.info(f"Created new canonical coin: {normalized_symbol} ({name})")
        else:
            # Update canonical coin metadata if needed
            canonical_coin.updated_at = datetime.utcnow()
        
        # Step 4: Create source mapping
        source_mapping = CoinSourceMapping(
            coin_id=canonical_coin.id,
            source=source,
            source_id=source_id,
            source_symbol=source_symbol or symbol,
            source_name=source_name or name,
            created_at=datetime.utcnow(),
            last_seen=datetime.utcnow()
        )
        db.add(source_mapping)
        
        try:
            db.commit()
            logger.info(
                f"Linked {source}:{source_id} to canonical coin "
                f"{canonical_coin.symbol} (ID: {canonical_coin.id})"
            )
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating coin/mapping: {e}")
            raise
        
        return canonical_coin
    
    @staticmethod
    def add_price_data(
        db: Session,
        coin: Coin,
        source: str,
        price_usd: float,
        market_cap_usd: Optional[float] = None,
        volume_24h_usd: Optional[float] = None,
        percent_change_24h: Optional[float] = None,
        source_timestamp: Optional[datetime] = None
    ) -> AssetPrice:
        """
        Add price data for a canonical coin.
        Links price to unified coin entity, not source-specific data.
        """
        
        price_record = AssetPrice(
            coin_id=coin.id,
            price_usd=price_usd,
            market_cap_usd=market_cap_usd,
            volume_24h_usd=volume_24h_usd,
            percent_change_24h=percent_change_24h,
            source=source,
            source_timestamp=source_timestamp,
            fetched_at=datetime.utcnow()
        )
        
        db.add(price_record)
        
        try:
            db.commit()
            db.refresh(price_record)
            return price_record
        except Exception as e:
            db.rollback()
            logger.error(f"Error adding price data: {e}")
            raise
    
    @staticmethod
    def get_coin_by_symbol(db: Session, symbol: str) -> Optional[Coin]:
        """Get canonical coin by symbol"""
        normalized_symbol = CoinNormalizationService.normalize_symbol(symbol)
        return db.query(Coin).filter(Coin.symbol == normalized_symbol).first()
    
    @staticmethod
    def get_coin_by_source_id(db: Session, source: str, source_id: str) -> Optional[Coin]:
        """Get canonical coin by source-specific ID"""
        mapping = db.query(CoinSourceMapping).filter(
            CoinSourceMapping.source == source,
            CoinSourceMapping.source_id == source_id
        ).first()
        
        return mapping.coin if mapping else None
    
    @staticmethod
    def get_latest_price(db: Session, coin_id: int) -> Optional[AssetPrice]:
        """Get most recent price for a canonical coin"""
        return db.query(AssetPrice).filter(
            AssetPrice.coin_id == coin_id
        ).order_by(AssetPrice.fetched_at.desc()).first()
    
    @staticmethod
    def get_all_sources_for_coin(db: Session, coin_id: int) -> list:
        """Get all source mappings for a canonical coin"""
        return db.query(CoinSourceMapping).filter(
            CoinSourceMapping.coin_id == coin_id
        ).all()


# ============= USAGE EXAMPLE IN ETL =============

def transform_coinpaprika_to_normalized(db: Session, raw_data: dict):
    """
    Example of how to use the normalization service in your ETL.
    Replace your current transformation logic with this pattern.
    """
    
    # Extract from raw data
    symbol = raw_data.get('symbol', '').upper()
    name = raw_data.get('name', '')
    source_id = raw_data.get('id', '')  # CoinPaprika's internal ID
    
    # Get or create canonical coin
    coin = CoinNormalizationService.get_or_create_coin(
        db=db,
        symbol=symbol,
        name=name,
        source='coinpaprika',
        source_id=source_id,
        source_symbol=raw_data.get('symbol'),
        source_name=raw_data.get('name')
    )
    
    # Add price data linked to canonical coin
    if 'price_usd' in raw_data and raw_data['price_usd'] is not None:
        CoinNormalizationService.add_price_data(
            db=db,
            coin=coin,
            source='coinpaprika',
            price_usd=raw_data['price_usd'],
            market_cap_usd=raw_data.get('market_cap_usd'),
            volume_24h_usd=raw_data.get('volume_24h_usd'),
            percent_change_24h=raw_data.get('percent_change_24h')
        )
    
    return coin


def transform_coingecko_to_normalized(db: Session, raw_data: dict):
    """Example for CoinGecko"""
    
    symbol = raw_data.get('symbol', '').upper()
    name = raw_data.get('name', '')
    source_id = raw_data.get('id', '')  # CoinGecko's internal ID
    
    coin = CoinNormalizationService.get_or_create_coin(
        db=db,
        symbol=symbol,
        name=name,
        source='coingecko',
        source_id=source_id,
        source_symbol=raw_data.get('symbol'),
        source_name=raw_data.get('name')
    )
    
    if 'current_price' in raw_data and raw_data['current_price'] is not None:
        CoinNormalizationService.add_price_data(
            db=db,
            coin=coin,
            source='coingecko',
            price_usd=raw_data['current_price'],
            market_cap_usd=raw_data.get('market_cap'),
            volume_24h_usd=raw_data.get('total_volume'),
            percent_change_24h=raw_data.get('price_change_percentage_24h')
        )
    
    return coin
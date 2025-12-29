from app.core.models import Coin, CoinSourceMapping
from sqlalchemy.orm import Session

def get_or_create_coin(
    db: Session,
    *,
    symbol: str,
    name: str,
    source: str,
    source_id: str,
    source_symbol: str | None = None,
    source_name: str | None = None
) -> Coin:
    canonical_symbol = symbol.upper().strip()

    # 1. Get or create canonical coin
    coin = (
        db.query(Coin)
        .filter(Coin.symbol == canonical_symbol)
        .first()
    )

    if not coin:
        coin = Coin(
            symbol=canonical_symbol,
            name=name.strip()
        )
        db.add(coin)
        db.commit()
        db.refresh(coin)

    # 2. Ensure source mapping exists
    mapping = (
        db.query(CoinSourceMapping)
        .filter_by(source=source, source_id=source_id)
        .first()
    )

    if not mapping:
        mapping = CoinSourceMapping(
            coin_id=coin.id,
            source=source,
            source_id=source_id,
            source_symbol=source_symbol,
            source_name=source_name
        )
        db.add(mapping)
        db.commit()

    return coin

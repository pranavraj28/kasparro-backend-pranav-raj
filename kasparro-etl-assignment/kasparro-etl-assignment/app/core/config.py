"""Application configuration using Pydantic settings."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database (Railway/Render will provide this automatically)
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/crypto_etl"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    PORT: Optional[int] = None  # For Railway/Render (they set PORT env var)
    
    # ETL
    ETL_INTERVAL_SECONDS: int = 300  # 5 minutes
    ETL_BATCH_SIZE: int = 100
    
    # Failure injection (for testing)
    FAIL_AFTER_N_RECORDS: Optional[int] = None
    
    # CSV Source
    CSV_SOURCE_PATH: Optional[str] = None
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # External APIs
    COINPAPRIKA_API_KEY: Optional[str] = None
    COINGECKO_API_KEY: Optional[str] = None
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
    }


settings = Settings()


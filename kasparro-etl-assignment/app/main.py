"""FastAPI application entry point."""
from fastapi import FastAPI
from app.api import routes, health, stats
from app.core.logging import logger
from app.core.db import Base, engine
from contextlib import asynccontextmanager
import asyncio
from app.services.etl_runner import ETLRunner
from app.core.db import SessionLocal
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting application...")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created/verified")
    
    # Start background ETL task
    async def run_etl_periodically():
        while True:
            try:
                db = SessionLocal()
                try:
                    etl_runner = ETLRunner(db)
                    result = etl_runner.run_all()
                    logger.info(f"ETL run completed: {result}")
                finally:
                    db.close()
            except Exception as e:
                logger.error(f"ETL run error: {e}", exc_info=True)
            
            await asyncio.sleep(settings.ETL_INTERVAL_SECONDS)
    
    # Start ETL task in background
    etl_task = asyncio.create_task(run_etl_periodically())
    
    yield
    
    # Shutdown
    etl_task.cancel()
    try:
        await etl_task
    except asyncio.CancelledError:
        pass
    logger.info("Application shutting down...")


app = FastAPI(
    title="Crypto ETL API",
    description="ETL system for cryptocurrency data ingestion",
    version="1.0.0",
    lifespan=lifespan,
)

# Register routers
app.include_router(routes.router, tags=["data"])
app.include_router(health.router, tags=["health"])
app.include_router(stats.router, tags=["stats"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Crypto ETL API",
        "version": "1.0.0",
        "docs": "/docs",
    }


#!/usr/bin/env python3
"""Verification script to check if the system is set up correctly."""
import sys
import os

def check_imports():
    """Check if all imports work."""
    print("🔍 Checking imports...")
    try:
        from app.core.config import settings
        from app.core.db import engine, SessionLocal
        from app.core.models import Asset, ETLCheckpoint
        from app.services.etl_runner import ETLRunner
        from app.api.routes import router
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def check_database_connection():
    """Check database connection."""
    print("\n🔍 Checking database connection...")
    try:
        from app.core.db import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("   Make sure PostgreSQL is running and DATABASE_URL is correct")
        return False

def check_tables():
    """Check if tables exist."""
    print("\n🔍 Checking database tables...")
    try:
        from app.core.db import Base, engine
        from sqlalchemy import inspect
        
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        required_tables = [
            'raw_coinpaprika',
            'raw_coingecko', 
            'raw_csv_source',
            'assets',
            'etl_checkpoints'
        ]
        
        missing = [t for t in required_tables if t not in tables]
        if missing:
            print(f"⚠️  Missing tables: {missing}")
            print("   Run: alembic upgrade head")
            return False
        else:
            print("✅ All required tables exist")
            return True
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False

def check_config():
    """Check configuration."""
    print("\n🔍 Checking configuration...")
    try:
        from app.core.config import settings
        print(f"   Database URL: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'configured'}")
        print(f"   ETL Interval: {settings.ETL_INTERVAL_SECONDS}s")
        print(f"   Batch Size: {settings.ETL_BATCH_SIZE}")
        print("✅ Configuration loaded")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def main():
    """Run all checks."""
    print("=" * 50)
    print("Kasparro ETL System - Setup Verification")
    print("=" * 50)
    
    results = []
    results.append(check_imports())
    results.append(check_config())
    results.append(check_database_connection())
    
    if results[2]:  # Only check tables if DB connection works
        results.append(check_tables())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ All checks passed! System is ready.")
        return 0
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())


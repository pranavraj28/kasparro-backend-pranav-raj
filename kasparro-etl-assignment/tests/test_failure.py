"""Tests for failure recovery."""
import pytest
import os
from app.core.models import Asset, ETLCheckpoint
from app.services.etl_runner import ETLRunner
from app.services.checkpoint import CheckpointService


def test_failure_mid_etl_resume_works(test_db):
    """Test that failure mid-ETL allows clean resume."""
    checkpoint_service = CheckpointService(test_db)
    
    # Set failure injection
    os.environ["FAIL_AFTER_N_RECORDS"] = "5"
    
    # Start ETL run
    run_id = checkpoint_service.start_run("test_source")
    assert run_id is not None
    
    # Simulate processing some records
    checkpoint_service.update_progress("test_source", 5)
    
    # Simulate failure
    checkpoint_service.fail_run("test_source", "Simulated failure")
    
    # Verify checkpoint preserved
    last_id = checkpoint_service.get_last_processed_id("test_source")
    assert last_id == 5
    
    # Resume should work from checkpoint
    checkpoint = checkpoint_service.get_checkpoint("test_source")
    assert checkpoint.last_processed_id == 5
    
    # Clean up
    os.environ.pop("FAIL_AFTER_N_RECORDS", None)


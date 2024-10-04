import pytest
import shutil
import os
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client

def remove_pycache_dirs():
    for root, dirs, files in os.walk("."):
        for d in dirs:
            if d == "__pycache__":
                pycache_path = os.path.join(root, d)
                shutil.rmtree(pycache_path)
            if d == ".pytest_cache":
                pytest_cache_path = os.path.join(root, d)
                shutil.rmtree(pytest_cache_path)

def pytest_sessionfinish(session, exitstatus):
    remove_pycache_dirs()
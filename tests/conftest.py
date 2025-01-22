import pytest
import os
import sys
sys.path.append('%s/../'%os.path.dirname(__file__))
from app import *
from fastapi.testclient import TestClient

@pytest.fixture(scope="session", autouse=True)
def delete_embedding_histories():
    if not os.path.exists(os.path.join(os.getcwd(), "outputs/embedding")):
        return
    for embedding in os.listdir(os.path.join(os.getcwd(), "outputs/embedding")):
        os.remove(os.path.join(os.getcwd(), "outputs/embedding", embedding))
      
        
@pytest.fixture(scope="session")
def client():
    with TestClient(app) as client:
        return client
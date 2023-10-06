from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.data.mongodb import connection
from main import app

client = TestClient(app=app)

def test_mongodb_connection():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "You are connected!"}
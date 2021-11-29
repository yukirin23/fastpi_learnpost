from fastapi.testclient import TestClient
from app import main


client = TestClient(app)


def test_root():
    res = client.get("/")
    print(res)

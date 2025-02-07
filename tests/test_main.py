from fastapi import status
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    response = client.get("/health")
    print(response.url)
    assert response.status_code == status.HTTP_200_OK

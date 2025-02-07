import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.main import create_app


@pytest.fixture
def app() -> FastAPI:
    return create_app()


@pytest.fixture
def client(app) -> TestClient:
    return TestClient(app, base_url="http://testserver")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# Test için SQLite kullan
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_short_url():
    response = client.post("/api/shorten", json={"original_url": "https://www.example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["original_url"] == "https://www.example.com/"
    assert "short_code" in data
    assert data["click_count"] == 0


def test_redirect():
    # Önce URL oluştur
    create_resp = client.post("/api/shorten", json={"original_url": "https://www.example.com"})
    short_code = create_resp.json()["short_code"]

    # Redirect test (follow_redirects=False ile)
    response = client.get(f"/{short_code}", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "https://www.example.com/"


def test_stats():
    create_resp = client.post("/api/shorten", json={"original_url": "https://www.example.com"})
    short_code = create_resp.json()["short_code"]

    # Bir kez tıkla
    client.get(f"/{short_code}", follow_redirects=False)

    # Stats kontrol et
    stats_resp = client.get(f"/api/{short_code}/stats")
    assert stats_resp.status_code == 200
    assert stats_resp.json()["click_count"] == 1


def test_delete():
    create_resp = client.post("/api/shorten", json={"original_url": "https://www.example.com"})
    short_code = create_resp.json()["short_code"]

    # Sil
    delete_resp = client.delete(f"/api/{short_code}")
    assert delete_resp.status_code == 200

    # Artık bulunamaz
    stats_resp = client.get(f"/api/{short_code}/stats")
    assert stats_resp.status_code == 404


def test_not_found():
    response = client.get("/api/nonexistent/stats")
    assert response.status_code == 404


def test_invalid_url():
    response = client.post("/api/shorten", json={"original_url": "not-a-url"})
    assert response.status_code == 422

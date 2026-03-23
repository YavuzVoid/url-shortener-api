# URL Shortener API

Uzun URL'leri kısaltan ve tıklama istatistiklerini takip eden RESTful API.

## Teknolojiler

- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **PostgreSQL / SQLite** - Veritabanı
- **Pytest** - Test framework
- **Docker** - Containerization

## Kurulum

```bash
git clone https://github.com/KULLANICI_ADIN/url-shortener-api.git
cd url-shortener-api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## API Endpoints

| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/health` | Sağlık kontrolü |
| POST | `/api/shorten` | Yeni kısa URL oluştur |
| GET | `/{short_code}` | Orijinal URL'ye yönlendir |
| GET | `/api/{short_code}/stats` | Tıklama istatistikleri |
| DELETE | `/api/{short_code}` | Kısa URL'yi sil |

## Kullanım

### URL Kısalt
```bash
curl -X POST http://localhost:8000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://www.example.com/uzun-url"}'
```

### İstatistikleri Gör
```bash
curl http://localhost:8000/api/abc123/stats
```

## Testler

```bash
pytest tests/ -v
```

## Docker

```bash
docker build -t url-shortener .
docker run -p 8000:8000 url-shortener
```

## API Dokümantasyonu

Uygulama çalışırken:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

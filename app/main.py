from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models.url import URL
from app.routes.url import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="Uzun URL'leri kısaltan ve tıklama istatistiklerini takip eden API",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


# API endpoint'leri /api prefix'i altında
app.include_router(router, prefix="/api")


# Redirect endpoint'i root'ta (kısa URL'ler için)
@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.short_code == short_code).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="Kısa URL bulunamadı")
    db_url.click_count += 1
    db.commit()
    return RedirectResponse(url=db_url.original_url)

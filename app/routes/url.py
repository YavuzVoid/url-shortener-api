import string
import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.url import URL
from app.schemas.url import URLCreate, URLResponse, URLStats
from app.config import BASE_URL

router = APIRouter()


def generate_short_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


@router.post("/shorten", response_model=URLResponse)
def create_short_url(url_data: URLCreate, db: Session = Depends(get_db)):
    short_code = generate_short_code()

    while db.query(URL).filter(URL.short_code == short_code).first():
        short_code = generate_short_code()

    db_url = URL(original_url=str(url_data.original_url), short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return URLResponse(
        id=db_url.id,
        original_url=db_url.original_url,
        short_code=db_url.short_code,
        short_url=f"{BASE_URL}/{db_url.short_code}",
        click_count=db_url.click_count,
        created_at=db_url.created_at,
    )


@router.get("/{short_code}/stats", response_model=URLStats)
def get_url_stats(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.short_code == short_code).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="Kısa URL bulunamadı")
    return db_url


@router.delete("/{short_code}")
def delete_url(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.short_code == short_code).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="Kısa URL bulunamadı")
    db.delete(db_url)
    db.commit()
    return {"message": "URL başarıyla silindi"}

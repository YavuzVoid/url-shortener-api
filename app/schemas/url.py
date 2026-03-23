from pydantic import BaseModel, HttpUrl
from datetime import datetime


class URLCreate(BaseModel):
    original_url: HttpUrl


class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    short_url: str
    click_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class URLStats(BaseModel):
    original_url: str
    short_code: str
    click_count: int
    created_at: datetime

    model_config = {"from_attributes": True}

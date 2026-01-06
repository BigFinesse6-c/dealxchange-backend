# backend/app/schemas/request.py
from pydantic import BaseModel
from datetime import datetime

class RequestBase(BaseModel):
    message: str | None = None

class RequestCreate(RequestBase):
    listing_id: int

class RequestOut(RequestBase):
    id: int
    listing_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2


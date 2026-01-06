from pydantic import BaseModel
from enum import Enum
from typing import Optional

class DealStatus(str, Enum):
    PENDING = "pending"
    REQUESTED = "requested"
    CLOSED = "closed"

class DealCreate(BaseModel):
    listing_id: int
    buyer_id: int
    status: Optional[DealStatus] = DealStatus.PENDING
    price: float
    arv: Optional[float]

    class Config:
        orm_mode = True  # for SQLAlchemy compatibility

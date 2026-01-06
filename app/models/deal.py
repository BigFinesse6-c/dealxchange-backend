from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum

Base = declarative_base()

class DealStatus(str, enum.Enum):
    requested = "requested"
    intro_paid = "intro_paid"
    intro_sent = "intro_sent"
    connected = "connected"
    under_review = "under_review"
    closed = "closed"
    canceled = "canceled"

class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"))
    buyer_id = Column(Integer, ForeignKey("users.id"))

    property_id = Column(Integer, nullable=False)
    buyer_name = Column(String, nullable=False)
    buyer_email = Column(String, nullable=False)
    message = Column(String, nullable=True)

    intro_fee = Column(Float, default=19.99)
    status = Column(Enum(DealStatus), default=DealStatus.requested)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    


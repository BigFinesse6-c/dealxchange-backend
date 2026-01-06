# app/models/listing.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from app.db.database import Base
from app.models.request import Request

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    address = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    year_built = Column(Integer, nullable=True)
    square_footage = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    image_urls = Column(JSONB, default=[])
    arv = Column(Integer, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved = Column(Boolean, default=False, nullable=False)  # <-- added field
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="listings")
    requests = relationship("Request", back_populates="listing", cascade="all, delete-orphan")
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    
class ListingImage(Base):
    __tablename__ = "listing_images"
    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey("listings.id"))
    url = Column(String, nullable=False)

    listing = relationship("Listing", back_populates="images")

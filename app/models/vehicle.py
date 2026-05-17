from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, Boolean, Enum, DateTime, ForeignKey
from app.database.database import Base

class Listing(Base):
    __tablename__ = "listings"

    id           = Column(Integer, primary_key=True, index=True)
    seller_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    make         = Column(String(100), nullable=False)
    model        = Column(String(100), nullable=False)
    year         = Column(Integer, nullable=False)
    mileage      = Column(Integer, nullable=False)
    price        = Column(Float, nullable=False)
    fuel_type    = Column(Enum("petrol", "diesel", "electric", "hybrid", name="fuel_type"), nullable=False)
    transmission = Column(Enum("manual", "automatic", name="transmission_type"), nullable=False)
    body_type    = Column(String(50), nullable=True)
    color        = Column(String(50), nullable=True)
    vin          = Column(String(17), unique=True, nullable=True)
    description  = Column(Text, nullable=True)
    location     = Column(String(150), nullable=True)
    status       = Column(Enum("available", "under_offer", "sold", name="listing_status"), default="available", nullable=False)
    created_at   = Column(DateTime, default=datetime.utcnow)
    updated_at   = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ListingImage(Base):
    __tablename__ = "listing_images"

    id         = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.id"), nullable=False)
    url        = Column(String(500), nullable=False)
    image_type = Column(Enum("exterior", "interior", "engine", "odometer", "other", name="image_type"), default="other", nullable=False)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
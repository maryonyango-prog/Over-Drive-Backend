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
from datetime import datetime
from app.database.database import db


class Vehicle(db.Model):
    __tablename__ = "vehicles"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    asking_price = db.Column(db.Float, nullable=False)

    fuel_type = db.Column(db.String(20))
    transmission = db.Column(db.String(20))

    previous_owners = db.Column(db.Integer, default=1)
    service_history_available = db.Column(db.Boolean, default=False)
    accident_history = db.Column(db.Boolean, default=False)

    # Analysis results
    age_years = db.Column(db.Integer)
    annual_mileage = db.Column(db.Float)
    condition_score = db.Column(db.Integer)
    risk_level = db.Column(db.String(20))
    price_assessment = db.Column(db.String(20))
    recommendation = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "mileage": self.mileage,
            "asking_price": self.asking_price,
            "fuel_type": self.fuel_type,
            "transmission": self.transmission,
            "previous_owners": self.previous_owners,
            "service_history_available": self.service_history_available,
            "accident_history": self.accident_history,
            "age_years": self.age_years,
            "annual_mileage": self.annual_mileage,
            "condition_score": self.condition_score,
            "risk_level": self.risk_level,
            "price_assessment": self.price_assessment,
            "recommendation": self.recommendation,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

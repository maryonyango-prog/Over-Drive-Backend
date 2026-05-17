from datetime import datetime
from sqlalchemy import Column, Integer, Float, Text, DateTime, ForeignKey
from sqlalchemy.dialects.sqlite import JSON
from app.database.database import Base

class Valuation(Base):
    __tablename__ = "valuations"

    id              = Column(Integer, primary_key=True, index=True)
    listing_id      = Column(Integer, ForeignKey("listings.id"), unique=True, nullable=False)
    condition_score = Column(Float, nullable=False)
    price_low       = Column(Float, nullable=False)
    price_mid       = Column(Float, nullable=False)
    price_high      = Column(Float, nullable=False)
    summary         = Column(Text, nullable=True)
    positives       = Column(JSON, nullable=True)
    concerns        = Column(JSON, nullable=True)
    created_at      = Column(DateTime, default=datetime.utcnow)
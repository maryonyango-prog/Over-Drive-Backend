from datetime import datetime
from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey, String, Float
from app.database.database import Base

class Message(Base):
    __tablename__ = "messages"

    id          = Column(Integer, primary_key=True, index=True)
    listing_id  = Column(Integer, ForeignKey("listings.id"), nullable=False)
    sender_id   = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content     = Column(Text, nullable=False)
    is_read     = Column(Boolean, default=False)
    created_at  = Column(DateTime, default=datetime.utcnow)

class SavedSearch(Base):
    __tablename__ = "saved_searches"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    make       = Column(String(100), nullable=True)
    model      = Column(String(100), nullable=True)
    min_price  = Column(Float, nullable=True)
    max_price  = Column(Float, nullable=True)
    fuel_type  = Column(String(50), nullable=True)
    body_type  = Column(String(50), nullable=True)
    location   = Column(String(150), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

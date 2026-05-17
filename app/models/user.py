from datetime import datetime
from sqlalchemy import Column, Integer, String, Enum, DateTime
from app.database.database import Base

class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(100), nullable=False)
    email      = Column(String(150), unique=True, index=True, nullable=False)
    password   = Column(String(255), nullable=False)
    role       = Column(Enum("buyer", "seller", name="user_role"), nullable=False)
    phone      = Column(String(20), nullable=True)
    location   = Column(String(150), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
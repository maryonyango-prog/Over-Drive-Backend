from datetime import datetime
from app.database.database import db


class Listing(db.Model):
    __tablename__ = "listings"

    id = db.Column(db.Integer, primary_key=True)

    # Optional: link to user (if you have users working)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    # Basic vehicle info
    title = db.Column(db.String(255), nullable=False)
    make = db.Column(db.String(100), nullable=True)
    model = db.Column(db.String(100), nullable=True)
    year = db.Column(db.Integer, nullable=True)

    mileage = db.Column(db.Integer, nullable=True)
    location = db.Column(db.String(255), nullable=True)

    # Status of analysis pipeline
    status = db.Column(db.String(50), default="pending")  
    # pending | processing | completed | failed

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
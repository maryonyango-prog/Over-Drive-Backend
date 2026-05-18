from datetime import datetime
from sqlalchemy.dialects.sqlite import JSON
from app.database.database import db


class Valuation(db.Model):
    __tablename__ = "valuations"

    id = db.Column(db.Integer, primary_key=True)

    listing_id = db.Column(
        db.Integer,
        db.ForeignKey("listings.id"),
        unique=True,
        nullable=False
    )

    condition_score = db.Column(db.Float, nullable=False)

    price_low = db.Column(db.Float, nullable=False)
    price_mid = db.Column(db.Float, nullable=False)
    price_high = db.Column(db.Float, nullable=False)

    summary = db.Column(db.Text, nullable=True)

    positives = db.Column(JSON, nullable=True)
    concerns = db.Column(JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
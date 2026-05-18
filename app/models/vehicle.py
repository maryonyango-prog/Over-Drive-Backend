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

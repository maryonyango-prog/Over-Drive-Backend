from datetime import datetime
from app.database.database import db

class Vehicle(db.Model):
    __tablename__ = "vehicle"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    make = db.Column(db.String(100))
    model = db.Column(db.String(100))
    year = db.Column(db.Integer)
    mileage = db.Column(db.Integer)
    asking_price = db.Column(db.Float)

    fuel_type = db.Column(db.String(50))
    transmission = db.Column(db.String(50))
    condition = db.Column(db.String(50))
    body_type = db.Column(db.String(50))
    engine_size = db.Column(db.Integer)
    color = db.Column(db.String(50))
    description = db.Column(db.Text)

    #  ADDED THIS LINE
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    images = db.relationship(
        "VehicleImage", 
        backref="vehicle", 
        lazy=True, 
        cascade="all, delete-orphan"
    )
    
    analysis = db.relationship(
        "VehicleAnalysis", 
        backref="vehicle", 
        uselist=False, 
        cascade="all, delete-orphan"
    )

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
            "condition": self.condition,
            "body_type": self.body_type,
            "engine_size": self.engine_size,
            "color": self.color,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
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

    previous_owners = db.Column(db.Integer, default=1)
    service_history_available = db.Column(db.Boolean, default=False)
    accident_history = db.Column(db.Boolean, default=False)

    # RELATIONSHIPS
    images = db.relationship(
        "VehicleImage",
        backref="vehicle",
        cascade="all, delete-orphan",
        lazy=True
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
            "previous_owners": self.previous_owners,
            "service_history_available": self.service_history_available,
            "accident_history": self.accident_history,
    }
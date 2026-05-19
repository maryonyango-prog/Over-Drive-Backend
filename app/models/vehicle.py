from app import db

class Vehicle(db.Model):
    __tablename__ = "vehicle"

    id = db.Column(db.Integer, primary_key=True)

    images = db.relationship(
        "VehicleImage",
        backref="vehicle",
        lazy=True,
        cascade="all, delete-orphan"
    )
from datetime import datetime
from app.database.database import db

class VehicleImage(db.Model):
    __tablename__ = "vehicle_images"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicle.id"), nullable=False, index=True)

    image_url = db.Column(db.String(500), nullable=False)
    public_id = db.Column(db.String(255), nullable=True)
    filename = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    image_type = db.Column(db.String(50), default="general")

    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "vehicle_id": self.vehicle_id,
            "image_url": self.image_url,
            "public_id": self.public_id,
            "filename": self.filename,
            "file_size": self.file_size,
            "image_type": self.image_type,
            "upload_date": self.upload_date.isoformat(),
        }
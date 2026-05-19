from datetime import datetime
from app.database.database import db

class VehicleImage(db.Model):
    __tablename__ = "vehicle_images"

    id = db.Column(db.Integer, primary_key=True)

    # 🔥 Correct FK to parent table
    vehicle_id = db.Column(
        db.Integer,
        db.ForeignKey("vehicles.id"),
        nullable=False,
        index=True
    )

    # Image metadata
    image_url = db.Column(db.String(255), nullable=False)
    image_type = db.Column(db.String(50), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "vehicle_id": self.vehicle_id,
            "image_url": self.image_url,
            "image_type": self.image_type,
            "filename": self.filename,
            "file_size": self.file_size,
            "upload_date": self.upload_date.isoformat()
        }
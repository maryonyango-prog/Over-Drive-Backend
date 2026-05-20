from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.database.database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(120), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)

    password_hash = db.Column(db.String(512), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # RELATIONSHIP
    vehicles = db.relationship("Vehicle", backref="owner", lazy=True)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "created_at": self.created_at.isoformat()
        }
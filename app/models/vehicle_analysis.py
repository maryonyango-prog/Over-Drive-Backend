from datetime import datetime
from app.database.database import db   

class VehicleAnalysis(db.Model):
    __tablename__ = "vehicle_analysis"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicle.id"), nullable=False)

    final_score = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(50), nullable=False)
    price_assessment = db.Column(db.String(100), nullable=False)

    rule_score = db.Column(db.Float, nullable=False)
    ai_penalty = db.Column(db.Float, nullable=False)

    ai_results = db.Column(db.JSON)
    recommendation = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "vehicle_id": self.vehicle_id,
            "final_score": self.final_score,
            "risk_level": self.risk_level,
            "price_assessment": self.price_assessment,
            "rule_score": self.rule_score,
            "ai_penalty": self.ai_penalty,
            "ai_results": self.ai_results,
            "recommendation": self.recommendation,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
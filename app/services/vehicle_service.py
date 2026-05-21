from app.database.database import db
from app.models.vehicle import Vehicle
from app.services.vehicle_analysis_service import VehicleAnalysisService


class VehicleService:

    @staticmethod
    def safe(value, default=None):
        return value if value not in [None, ""] else default

    @staticmethod
    def register_vehicle(data, owner_id):
        try:
            vehicle = Vehicle(
                owner_id=owner_id,
                make=data["make"],
                model=data["model"],
                year=int(data["year"]),
                mileage=int(data.get("mileage", 0)),

                asking_price=VehicleService.safe(data.get("asking_price"), 0),
                fuel_type=VehicleService.safe(data.get("fuel_type"), "Unknown"),
                transmission=VehicleService.safe(data.get("transmission"), "Unknown"),
                condition=VehicleService.safe(data.get("condition"), "Unknown"),
                body_type=VehicleService.safe(data.get("body_type"), "Unknown"),
                engine_size=VehicleService.safe(data.get("engine_size"), 0),
                color=VehicleService.safe(data.get("color"), "Unknown"),
            )

            db.session.add(vehicle)
            db.session.commit()

            return {
                "success": True,
                "vehicle": vehicle.to_dict()
            }, 201

        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def analyze_vehicle(vehicle_id):
        vehicle = Vehicle.query.get(vehicle_id)

        if not vehicle:
            return {"error": "Vehicle not found"}, 404

        return VehicleAnalysisService.analyze(vehicle)

    @staticmethod
    def create_draft_vehicle(owner_id):
        vehicle = Vehicle(
            owner_id=owner_id,
            is_draft=True
        )

        db.session.add(vehicle)
        db.session.commit()

        return {
            "success": True,
            "data": vehicle.to_dict()
        }, 201
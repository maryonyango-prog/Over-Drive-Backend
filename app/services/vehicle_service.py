# app/services/vehicle_service.py
from app.database.database import db
from app.models.vehicle import Vehicle

class VehicleService:

    @staticmethod
    def safe_int(value, default=0):
        try:
            return int(value) if value not in [None, "", "null"] else default
        except:
            return default

    @staticmethod
    def safe_float(value, default=0.0):
        try:
            return float(value) if value not in [None, "", "null"] else default
        except:
            return default

    @staticmethod
    def register_vehicle(data, owner_id):
        try:
            vehicle = Vehicle(
                owner_id=owner_id,
                make=data.get("make", "Unknown"),
                model=data.get("model", "Unknown"),
                year=VehicleService.safe_int(data.get("year")),
                mileage=VehicleService.safe_int(data.get("mileage")),
                asking_price=VehicleService.safe_float(data.get("asking_price")),
                fuel_type=data.get("fuel_type", "Unknown"),
                transmission=data.get("transmission", "Unknown"),
                condition=data.get("condition", "Unknown"),
                body_type=data.get("body_type", "Unknown"),
                engine_size=VehicleService.safe_int(data.get("engine_size")),
                color=data.get("color", "Unknown"),
                description=data.get("description", "No description provided"),
            )

            db.session.add(vehicle)
            db.session.commit()

            return {
                "success": True,
                "message": "Vehicle registered successfully",
                "vehicle": vehicle.to_dict()
            }, 201

        except Exception as e:
            db.session.rollback()
            print("Vehicle registration error:", str(e))
            return {"error": str(e), "message": "Failed to save vehicle"}, 400
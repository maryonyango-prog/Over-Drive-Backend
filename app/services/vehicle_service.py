from app.database.database import db
from app.models.vehicle import Vehicle
from app.services.vehicle_analysis_service import VehicleAnalysisService


class VehicleService:

    @staticmethod
    def register_vehicle(data, owner_id):

        vehicle = Vehicle(
            owner_id=owner_id,
            make=data["make"],
            model=data["model"],
            year=int(data["year"]),
            mileage=int(data["mileage"]),
            asking_price=float(data["asking_price"]),
        )

        db.session.add(vehicle)
        db.session.commit()

        return {
            "success": True,
            "vehicle": vehicle.to_dict()
        }, 201


    @staticmethod
    def analyze_vehicle(vehicle_id):

        vehicle = Vehicle.query.get(vehicle_id)

        if not vehicle:
            return {"error": "Vehicle not found"}, 404

        return VehicleAnalysisService.analyze(vehicle)
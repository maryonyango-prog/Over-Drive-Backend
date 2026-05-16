from app.database import db
from app.models.vehicle import Vehicle
from app.services.vehicle_analysis_service import VehicleAnalysisService


class VehicleService:
    @staticmethod
    def analyze_vehicle(data: dict):
        analysis = VehicleAnalysisService.analyze(data)
        return {
            "success": True,
            "analysis": analysis,
        }, 200

    @staticmethod
    def register_vehicle(data: dict, owner_id: int):
        analysis = VehicleAnalysisService.analyze(data)

        vehicle = Vehicle(
            owner_id=owner_id,
            make=data["make"],
            model=data["model"],
            year=int(data["year"]),
            mileage=int(data["mileage"]),
            asking_price=float(data["asking_price"]),
            fuel_type=data.get("fuel_type"),
            transmission=data.get("transmission"),
            previous_owners=int(data.get("previous_owners", 1)),
            service_history_available=bool(
                data.get("service_history_available", False)
            ),
            accident_history=bool(data.get("accident_history", False)),
            age_years=analysis["age_years"],
            annual_mileage=analysis["annual_mileage"],
            condition_score=analysis["condition_score"],
            risk_level=analysis["risk_level"],
            price_assessment=analysis["price_assessment"],
            recommendation=analysis["recommendation"],
        )

        db.session.add(vehicle)
        db.session.commit()

        return {
            "success": True,
            "message": "Vehicle registered successfully",
            "vehicle": vehicle.to_dict(),
        }, 201

    @staticmethod
    def get_vehicle(vehicle_id: int):
        vehicle = Vehicle.query.get(vehicle_id)

        if not vehicle:
            return {
                "success": False,
                "message": "Vehicle not found",
            }, 404

        return {
            "success": True,
            "vehicle": vehicle.to_dict(),
        }, 200
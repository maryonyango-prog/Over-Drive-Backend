from flask import Blueprint, request, jsonify, g
from app.database.database import db
from app.models.vehicle import Vehicle
from app.services.vehicle_service import VehicleService
from app.services.vehicle_analysis_service import VehicleAnalysisService
from app.utils.auth_utils import token_required

vehicle_bp = Blueprint("vehicle", __name__, url_prefix="/api/vehicle")


@vehicle_bp.route("/valuation", methods=["POST"])
@token_required
def create_valuation():
    """Create vehicle + run initial AI valuation"""
    data = request.get_json() or {}
    owner_id = g.current_user.id

    vehicle_response, status = VehicleService.register_vehicle(data, owner_id)
    if status != 201:
        return jsonify(vehicle_response), status

    vehicle_data = vehicle_response.get("vehicle") or vehicle_response.get("data")
    vehicle_id = vehicle_data.get("id")

    if not vehicle_id:
        return jsonify({"error": "Vehicle ID missing"}), 500

    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404

    # Run initial analysis
    analysis_response, analysis_status = VehicleAnalysisService.analyze(vehicle)

    return jsonify({
        "success": True,
        "vehicle": vehicle_data,
        "valuation": analysis_response
    }), 200


@vehicle_bp.route("/register", methods=["POST"])
@token_required
def register_vehicle():
    """Register vehicle only (without analysis)"""
    data = request.get_json() or {}
    owner_id = g.current_user.id
    response, status = VehicleService.register_vehicle(data, owner_id)
    return jsonify(response), status


@vehicle_bp.route("/<int:vehicle_id>/analyze", methods=["POST"])
@token_required
def analyze_vehicle(vehicle_id):
    """Manual analyze endpoint"""
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    if vehicle.owner_id != g.current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    response, status = VehicleAnalysisService.analyze(vehicle)
    return jsonify(response), status


@vehicle_bp.route("/<int:vehicle_id>/revalue", methods=["POST"])
@token_required
def revalue_vehicle(vehicle_id):
    """Re-run AI valuation on existing vehicle"""
    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    if vehicle.owner_id != g.current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    response, status = VehicleAnalysisService.analyze(vehicle)
    
    return jsonify({
        "success": True,
        "message": "Vehicle revalued successfully",
        "valuation": response
    }), status


@vehicle_bp.route("/history", methods=["GET"])
@token_required
def get_vehicle_history():
    """Get all vehicles with their analysis"""
    owner_id = g.current_user.id

    vehicles = Vehicle.query.filter_by(owner_id=owner_id)\
        .order_by(Vehicle.id.desc()).all()

    history = []
    for vehicle in vehicles:
        analysis_data = None
        if hasattr(vehicle, 'analysis') and vehicle.analysis:
            analysis_data = vehicle.analysis.to_dict()

        history.append({
            "id": vehicle.id,
            "make": vehicle.make,
            "model": vehicle.model,
            "year": vehicle.year,
            "mileage": vehicle.mileage,
            "asking_price": vehicle.asking_price,
            "fuel_type": vehicle.fuel_type,
            "transmission": vehicle.transmission,
            "condition": vehicle.condition,
            "body_type": vehicle.body_type,
            "engine_size": vehicle.engine_size,
            "color": vehicle.color,
            "description": vehicle.description,
            "created_at": vehicle.created_at.isoformat() if hasattr(vehicle, 'created_at') and vehicle.created_at else None,
            "images": [img.to_dict() for img in vehicle.images],
            "analysis": analysis_data
        })

    return jsonify({
        "success": True,
        "count": len(history),
        "history": history
    }), 200
from flask import Blueprint, request, jsonify
from app.services.vehicle_service import VehicleService

vehicle_bp = Blueprint("vehicle", __name__, url_prefix="/api/vehicle")


@vehicle_bp.route("/analyze", methods=["POST"])
def analyze_vehicle():
    data = request.get_json() or {}
    response, status = VehicleService.analyze_vehicle(data)
    return jsonify(response), status


@vehicle_bp.route("/register", methods=["POST"])
def register_vehicle():
    data = request.get_json() or {}

    # Replace with JWT current user later.
    owner_id = data.get("owner_id", 1)

    response, status = VehicleService.register_vehicle(data, owner_id)
    return jsonify(response), status


@vehicle_bp.route("/<int:vehicle_id>", methods=["GET"])
def get_vehicle(vehicle_id):
    response, status = VehicleService.get_vehicle(vehicle_id)
    return jsonify(response), status
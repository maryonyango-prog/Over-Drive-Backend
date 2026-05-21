import os

from flask import Blueprint, request, jsonify, current_app, send_from_directory, g
from werkzeug.utils import secure_filename

from app.database.database import db
from app.models.vehicle_image import VehicleImage
from app.models.vehicle import Vehicle
from app.services.vehicle_service import VehicleService
from app.utils.auth_utils import token_required


vehicle_bp = Blueprint("vehicle", __name__, url_prefix="/api/vehicle")


# -------------------------------------------------
# VALUATION (SECURED)
# -------------------------------------------------
@vehicle_bp.route("/valuation", methods=["POST"])
@token_required
def create_valuation():

    data = request.get_json() or {}
    owner_id = g.current_user.id

    vehicle_response, status = VehicleService.register_vehicle(data, owner_id)

    if status != 201:
        return jsonify(vehicle_response), status

    vehicle_data = (
        vehicle_response.get("data")
        or vehicle_response.get("vehicle")
        or vehicle_response
    )

    vehicle_id = vehicle_data.get("id")

    if not vehicle_id:
        return jsonify({"error": "Vehicle ID missing"}), 500

    analysis_response, analysis_status = VehicleService.analyze_vehicle(vehicle_id)

    if analysis_status != 200:
        return jsonify(analysis_response), analysis_status

    valuation_data = (
        analysis_response.get("data")
        or analysis_response
    )

    return jsonify({
        "id": vehicle_id,
        "vehicle": vehicle_data,
        "valuation": valuation_data
    }), 200


# -------------------------------------------------
# REGISTER VEHICLE (SECURED)
# -------------------------------------------------
@vehicle_bp.route("/register", methods=["POST"])
@token_required
def register_vehicle():

    data = request.get_json() or {}
    owner_id = g.current_user.id

    response, status = VehicleService.register_vehicle(data, owner_id)

    return jsonify(response), status


# -------------------------------------------------
# ANALYZE VEHICLE (SECURED + OWNERSHIP CHECK)
# -------------------------------------------------
@vehicle_bp.route("/<int:vehicle_id>/analyze", methods=["POST"])
@token_required
def analyze_vehicle(vehicle_id):

    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404

    if vehicle.owner_id != g.current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    response, status = VehicleService.analyze_vehicle(vehicle_id)

    return jsonify(response), status


# -------------------------------------------------
# GET VEHICLE (SECURED)
# -------------------------------------------------
@vehicle_bp.route("/<int:vehicle_id>", methods=["GET"])
@token_required
def get_vehicle(vehicle_id):

    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404

    if vehicle.owner_id != g.current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    response, status = VehicleService.get_vehicle(vehicle_id)

    return jsonify(response), status


# -------------------------------------------------
# UPLOAD IMAGE (SECURED)
# -------------------------------------------------
@vehicle_bp.route("/<int:vehicle_id>/upload_image", methods=["POST"])
@token_required
def upload_vehicle_image(vehicle_id):

    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404

    if vehicle.owner_id != g.current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    file = request.files.get("image")

    if not file:
        return jsonify({"error": "No image file provided"}), 400

    filename = secure_filename(file.filename)

    upload_folder = current_app.config.get("UPLOAD_FOLDER", "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)

    file_size = os.path.getsize(file_path)
    image_type = file.content_type or "unknown"

    image_url = f"/uploads/{filename}"

    new_image = VehicleImage(
        vehicle_id=vehicle_id,
        image_url=image_url,
        image_type=image_type,
        filename=filename,
        file_size=file_size
    )

    db.session.add(new_image)
    db.session.commit()

    return jsonify({
        "message": "Image uploaded successfully",
        "data": new_image.to_dict()
    }), 201


# -------------------------------------------------
# SERVE FILES
# -------------------------------------------------
@vehicle_bp.route("/uploads/<filename>")
def serve_uploaded_file(filename):

    upload_folder = current_app.config.get("UPLOAD_FOLDER", "uploads")
    return send_from_directory(upload_folder, filename)


# -------------------------------------------------
# DRAFT VEHICLE (SECURED)
# -------------------------------------------------
@vehicle_bp.route("/draft", methods=["POST"])
@token_required
def create_draft_vehicle():

    owner_id = g.current_user.id

    response, status = VehicleService.create_draft_vehicle(owner_id)

    return jsonify(response), status


# -------------------------------------------------
# VALUATION FETCH (SECURED)
# -------------------------------------------------
@vehicle_bp.route("/<int:vehicle_id>/valuation", methods=["GET"])
@token_required
def get_vehicle_valuation(vehicle_id):

    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404

    if vehicle.owner_id != g.current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    analysis_data = None

    if vehicle.analysis:
        analysis_data = vehicle.analysis.to_dict()

    return jsonify({
        "id": vehicle.id,
        "owner_id": vehicle.owner_id,
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
        "previous_owners": vehicle.previous_owners,
        "service_history_available": vehicle.service_history_available,
        "accident_history": vehicle.accident_history,
        "images": [img.to_dict() for img in vehicle.images],
        "analysis": analysis_data
    }), 200
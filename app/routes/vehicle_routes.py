import os

from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename

from app.database.database import db
from app.models import vehicle
from app.models.vehicle_image import VehicleImage
from app.services.vehicle_service import VehicleService
from app.models.vehicle import Vehicle


vehicle_bp = Blueprint("vehicle", __name__, url_prefix="/api/vehicle")


# -------------------------------------------------
# NEW: FRONTEND-COMPATIBLE AI VALUATION ENDPOINT
# -------------------------------------------------
@vehicle_bp.route("/valuation", methods=["POST"])
def create_valuation():
    """
    Frontend single-step flow:
    create vehicle → run AI → return valuation
    """

    data = request.get_json() or {}
    owner_id = data.get("owner_id", 1)

    # 1. Create vehicle
    vehicle_response, status = VehicleService.register_vehicle(data, owner_id)

    if status != 201:
        return jsonify(vehicle_response), status

    # -----------------------------
    # SAFE EXTRACTION (NO CRASH)
    # -----------------------------
    vehicle_data = None

    if isinstance(vehicle_response, dict):
        vehicle_data = (
            vehicle_response.get("data")
            or vehicle_response.get("vehicle")
            or vehicle_response
        )

    if not isinstance(vehicle_data, dict):
        return jsonify({
            "error": "Invalid vehicle response format",
            "debug": str(vehicle_response)
        }), 500

    vehicle_id = vehicle_data.get("id")

    if not vehicle_id:
        return jsonify({
            "error": "Vehicle ID missing after creation",
            "debug": vehicle_data
        }), 500

    # 2. Run AI analysis
    analysis_response, analysis_status = VehicleService.analyze_vehicle(vehicle_id)

    if analysis_status != 200:
        return jsonify(analysis_response), analysis_status

    # 3. Normalize AI response safely
    valuation_data = None

    if isinstance(analysis_response, dict):
        valuation_data = (
            analysis_response.get("data")
            or analysis_response
        )
    else:
        valuation_data = analysis_response

    # 4. Final response
    return jsonify({
        "id": vehicle_id,
        "vehicle": vehicle_data,
        "valuation": valuation_data
    }), 200


# -------------------------------------------------
# EXISTING ROUTES (KEPT FOR BACKWARD COMPATIBILITY)
# -------------------------------------------------

@vehicle_bp.route("/<int:vehicle_id>/analyze", methods=["POST"])
def analyze_vehicle(vehicle_id):
    response, status = VehicleService.analyze_vehicle(vehicle_id)
    return jsonify(response), status


@vehicle_bp.route("/register", methods=["POST"])
def register_vehicle():
    data = request.get_json() or {}

    owner_id = data.get("owner_id", 1)

    response, status = VehicleService.register_vehicle(data, owner_id)
    return jsonify(response), status


@vehicle_bp.route("/<int:vehicle_id>", methods=["GET"])
def get_vehicle(vehicle_id):
    response, status = VehicleService.get_vehicle(vehicle_id)
    return jsonify(response), status


# -------------------------------------------------
# IMAGE UPLOAD ROUTE
# -------------------------------------------------

@vehicle_bp.route("/<int:vehicle_id>/upload_image", methods=["POST"])
def upload_vehicle_image(vehicle_id):
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
# SERVE UPLOADED FILES
# -------------------------------------------------

@vehicle_bp.route("/uploads/<filename>")
def serve_uploaded_file(filename):
    upload_folder = current_app.config.get("UPLOAD_FOLDER", "uploads")
    return send_from_directory(upload_folder, filename)

@vehicle_bp.route("/draft", methods=["POST"])
def create_draft_vehicle():
    data = request.get_json() or {}
    owner_id = data.get("owner_id", 1)

    vehicle, status = VehicleService.create_draft_vehicle(owner_id)
    return jsonify(vehicle), status

@vehicle_bp.route("/<int:vehicle_id>/valuation", methods=["GET"])
def get_vehicle_valuation(vehicle_id):

    vehicle = Vehicle.query.get(vehicle_id)

    if not vehicle:
        return jsonify({
            "error": "Vehicle not found"
        }), 404

    analysis_data = None

    if vehicle.analysis:
        analysis_data = vehicle.analysis.to_dict() if vehicle.analysis else None    

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

    "images": [
        image.to_dict()
        for image in vehicle.images
    ],

    "analysis": analysis_data
}), 200
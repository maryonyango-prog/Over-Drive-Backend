import os

from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename

from app.database.database import db
from app.models.vehicle_image import VehicleImage
from app.services.vehicle_service import VehicleService


vehicle_bp = Blueprint("vehicle", __name__, url_prefix="/api/vehicle")


# -------------------------
# VEHICLE ROUTES
# -------------------------

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


# -------------------------
# IMAGE UPLOAD ROUTE
# -------------------------

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

    # IMPORTANT FIX: use consistent URL (no request.host_url needed)
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


# -------------------------
# SERVE UPLOADED FILES
# -------------------------

@vehicle_bp.route("/uploads/<filename>")
def serve_uploaded_file(filename):
    upload_folder = current_app.config.get("UPLOAD_FOLDER", "uploads")
    return send_from_directory(upload_folder, filename)
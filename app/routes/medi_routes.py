# app/routes/media_routes.py

from flask import Blueprint, request, jsonify
from app.services.media_service import MediaService
from app.utils.file_utils import allowed_file

media_bp = Blueprint("media", __name__, url_prefix="/api/media")


@media_bp.route("/vehicles/<int:vehicle_id>/upload", methods=["POST"])
def upload_vehicle_image(vehicle_id):
    # Check if file was sent
    if "image" not in request.files:
        return jsonify({
            "success": False,
            "message": "No image file provided"
        }), 400

    file = request.files["image"]

    # Check if filename is empty
    if file.filename == "":
        return jsonify({
            "success": False,
            "message": "No file selected"
        }), 400

    # Validate file type
    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "message": "Invalid file type. Allowed: png, jpg, jpeg"
        }), 400

    # Optional image type (front, rear, interior, engine, damage, general)
    image_type = request.form.get("image_type", "general")

    response, status = MediaService.upload_vehicle_image(
        vehicle_id,
        file,
        image_type
    )

    return jsonify(response), status


@media_bp.route("/vehicles/<int:vehicle_id>/images", methods=["GET"])
def get_vehicle_images(vehicle_id):
    response, status = MediaService.get_vehicle_images(vehicle_id)
    return jsonify(response), status


@media_bp.route("/images/<int:image_id>", methods=["DELETE"])
def delete_image(image_id):
    response, status = MediaService.delete_image(image_id)
    return jsonify(response), status
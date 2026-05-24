# app/routes/media_routes.py

from flask import Blueprint, request, jsonify
from app.models.vehicle_image import VehicleImage
from app.utils.file_utils import allowed_file
from app.services.media_service import MediaService
from app.utils.auth_utils import token_required

media_bp = Blueprint("media", __name__, url_prefix="/api/media")


@media_bp.route("/vehicles/<int:vehicle_id>/upload", methods=["POST"])
@token_required
def upload_vehicle_image(vehicle_id):
    """Upload image for a specific vehicle"""
    if "image" not in request.files:
        return jsonify({"success": False, "message": "No image file provided"}), 400
    
    file = request.files["image"]
    
    if file.filename == "":
        return jsonify({"success": False, "message": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "message": "Invalid file type. Allowed: png, jpg, jpeg, webp"
        }), 400

    response, status = MediaService.save_vehicle_image(file, vehicle_id)
    return jsonify(response), status


@media_bp.route("/vehicles/<int:vehicle_id>/images", methods=["GET"])
def get_vehicle_images(vehicle_id):
    """Get all images for a vehicle"""
    response, status = MediaService.get_vehicle_images(vehicle_id)
    return jsonify(response), status


@media_bp.route("/images/<int:image_id>", methods=["DELETE"])
@token_required
def delete_image(image_id):
    """Delete an image"""
    response, status = MediaService.delete_image(image_id)
    return jsonify(response), status


# ==================== DEBUG ROUTE ====================
@media_bp.route("/debug-images", methods=["GET"])
def debug_images():
    """Debug: Show all images in database"""
    images = VehicleImage.query.all()
    return jsonify({
        "total": len(images),
        "images": [img.to_dict() for img in images]
    })


# ==================== TEST CLOUDINARY ROUTE ====================
@media_bp.route("/test-cloudinary", methods=["GET"])
def test_cloudinary():
    """Test Cloudinary connection"""
    try:
        from app.utils.file_utils import upload_to_cloudinary
        from io import BytesIO
        import base64

        # Minimal valid JPEG for testing
        test_base64 = b'/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAAQABADASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAb/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAH/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdAB//2Q=='
        test_jpeg = base64.b64decode(test_base64)
        test_file = BytesIO(test_jpeg)
        test_file.filename = "test.jpg"

        result = upload_to_cloudinary(test_file, folder="test")

        if result.get("success"):
            return jsonify({
                "success": True,
                "message": "Cloudinary test successful",
                "url": result.get("url")
            })
        else:
            return jsonify({
                "success": False,
                "message": "Upload failed",
                "error": result.get("error")
            }), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Test failed",
            "error": str(e)
        }), 500


# ==================== MIGRATION ROUTE ====================
@media_bp.route("/migrate-to-cloudinary", methods=["POST"])
def migrate_to_cloudinary():
    """Migrate local images to Cloudinary"""
    try:
        from app import db
        from app.models.vehicle_image import VehicleImage
        from app.utils.file_utils import upload_to_cloudinary
        from io import BytesIO
        import os

        images = VehicleImage.query.all()
        print(f"Found {len(images)} images to check.")

        migrated = 0
        skipped = 0
        failed = 0

        for img in images:
            if img.image_url and img.image_url.startswith("https://"):
                skipped += 1
                continue

            filename = os.path.basename(img.image_url.lstrip("/"))
            local_path = os.path.join("uploads", filename)

            if not os.path.exists(local_path):
                print(f"Missing: {filename}")
                failed += 1
                continue

            try:
                with open(local_path, "rb") as f:
                    file_obj = BytesIO(f.read())
                    file_obj.filename = filename

                result = upload_to_cloudinary(file_obj, folder="vehicles")

                if result and result.get("success"):
                    img.image_url = result["url"]
                    img.public_id = result.get("public_id")
                    db.session.commit()
                    print(f"Migrated: {filename}")
                    migrated += 1
                else:
                    failed += 1
            except Exception as e:
                print(f"Error migrating {filename}: {e}")
                failed += 1
                db.session.rollback()

        return jsonify({
            "success": True,
            "message": "Migration completed",
            "migrated": migrated,
            "skipped": skipped,
            "failed": failed
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
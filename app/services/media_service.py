import os

from app.database.database import db
from app.models.vehicle import Vehicle
from app.models.vehicle_image import VehicleImage
from app.utils.file_utils import save_file


class MediaService:
    @staticmethod
    def save_vehicle_image(vehicle_id, file, image_type="general"):
        # Check if vehicle exists
        vehicle = Vehicle.query.get(vehicle_id)

        if not vehicle:
            return {
                "success": False,
                "message": "Vehicle not found"
            }, 404

        # Save file to uploads folder
        file_data = save_file(file, "uploads")

        # Create database record
        image = VehicleImage(
            vehicle_id=vehicle_id,
            image_url=file_data["file_path"],   
            filename=file_data["filename"],
            file_size=file_data["file_size"],
            image_type=image_type
        )

        db.session.add(image)
        db.session.commit()

        return {
            "success": True,
            "message": "Image uploaded successfully",
            "data": image.to_dict()
        }, 201

    @staticmethod
    def get_vehicle_images(vehicle_id):
        images = VehicleImage.query.filter_by(
            vehicle_id=vehicle_id
        ).all()

        return {
            "success": True,
            "data": [image.to_dict() for image in images]
        }, 200

    @staticmethod
    def delete_image(image_id):
        image = VehicleImage.query.get(image_id)

        if not image:
            return {
                "success": False,
                "message": "Image not found"
            }, 404

        # Delete file from disk
        if image.image_url and os.path.exists(image.image_url):
            os.remove(image.image_url)

        # Delete database record
        db.session.delete(image)
        db.session.commit()

        return {
            "success": True,
            "message": "Image deleted successfully"
        }, 200
from app.models.vehicle_image import VehicleImage
from app.database.database import db
from app.utils.file_utils import upload_to_cloudinary

class MediaService:

    @staticmethod
    def save_vehicle_image(file, vehicle_id):
        try:
            if not file or not vehicle_id:
                return {"success": False, "message": "Missing file or vehicle_id"}, 400

            result = upload_to_cloudinary(file, folder="vehicles")
            
            if not result or not result.get("success"):
                return {"success": False, "message": "Cloudinary upload failed"}, 500

            vehicle_image = VehicleImage(
                vehicle_id=vehicle_id,
                image_url=result["url"],
                public_id=result.get("public_id"),
                filename=result.get("filename") or file.filename,
                file_size=result.get("file_size") or 0,
                image_type=getattr(file, 'content_type', "image/jpeg")
            )
            
            db.session.add(vehicle_image)
            db.session.commit()
            
            print(f" Image saved to DB: {result['url']}")
            
            return {
                "success": True,
                "message": "Image uploaded successfully",
                "image": vehicle_image.to_dict()
            }, 201

        except Exception as e:
            print(f" Error saving vehicle image: {str(e)}")
            db.session.rollback()
            return {"success": False, "message": str(e)}, 500
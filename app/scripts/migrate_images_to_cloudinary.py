# app/scripts/migrate_images_to_cloudinary.py

import os
from io import BytesIO
import sys

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import create_app, db
from app.models.vehicle_image import VehicleImage
from app.utils.file_utils import upload_to_cloudinary


def migrate_images():
    # Create app and force initialization
    app = create_app()
    
    # Force db initialization if needed
    if not hasattr(db, 'engine') or db.engine is None:
        db.init_app(app)
    
    with app.app_context():
        # Determine uploads folder
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        uploads_dir = os.path.join(base_dir, "uploads")
        
        print(f"🔍 Searching images in: {uploads_dir}")
        if not os.path.exists(uploads_dir):
            print(f" Uploads folder not found at: {uploads_dir}")
            return

        try:
            images = VehicleImage.query.all()
            print(f" Found {len(images)} images in database.\n")
        except Exception as e:
            print(f" Database query failed: {e}")
            print("Make sure your database is running and connected.")
            return

        migrated = 0
        skipped = 0
        failed = 0
        missing = 0

        for img in images:
            if img.image_url and img.image_url.startswith("https://"):
                skipped += 1
                continue

            filename = os.path.basename(img.image_url.lstrip("/"))
            local_path = os.path.join(uploads_dir, filename)

            try:
                if not os.path.exists(local_path):
                    print(f" Missing file: {filename}")
                    missing += 1
                    continue

                print(f" Processing: {filename}")

                with open(local_path, "rb") as f:
                    file_obj = BytesIO(f.read())
                    file_obj.filename = filename

                result = upload_to_cloudinary(file_obj, folder="vehicles")

                if result and result.get("success"):
                    img.image_url = result["url"]
                    img.public_id = result.get("public_id")
                    db.session.commit()
                    print(f" Migrated: {filename}")
                    migrated += 1
                else:
                    print(f" Upload failed: {filename}")
                    failed += 1

            except Exception as e:
                print(f" Error with {filename}: {str(e)}")
                failed += 1
                db.session.rollback()

        print("\n" + "="*70)
        print("MIGRATION COMPLETE")
        print("="*70)
        print(f" Successfully migrated : {migrated}")
        print(f"⏭ Skipped (already cloud): {skipped}")
        print(f"  Missing files         : {missing}")
        print(f" Failed                 : {failed}")
        print("="*70)


if __name__ == "__main__":
    migrate_images()
# app/services/media_service.py

import os
from werkzeug.utils import secure_filename
from app.config import Config
from app import db
from app.models.vehicle_image import VehicleImage


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def save_vehicle_image(file, vehicle_id):
    if not allowed_file(file.filename):
        return None, "Invalid file type"

    filename = secure_filename(file.filename)

    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

    file_path = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(file_path)

    image = VehicleImage(
        vehicle_id=vehicle_id,
        file_path=file_path
    )

    db.session.add(image)
    db.session.commit()

    return image, None
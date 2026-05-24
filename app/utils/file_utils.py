# app/utils/file_utils.py

import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
import cloudinary
import cloudinary.uploader
from io import BytesIO


def allowed_file(filename):
    """Check if file extension is allowed"""
    if not filename:
        return False
    allowed_extensions = {'png', 'jpg', 'jpeg', 'webp'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def upload_to_cloudinary(file, folder="vehicles"):
    """
    Upload file to Cloudinary and return result
    Works with both real uploaded files and BytesIO test files
    """
    try:
        # Configure Cloudinary (in case it wasn't configured globally)
        cloudinary.config(
            cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
            api_key=os.getenv('CLOUDINARY_API_KEY'),
            api_secret=os.getenv('CLOUDINARY_API_SECRET'),
            secure=True
        )

        # Generate unique public_id
        public_id = str(uuid.uuid4())

        # Prepare file for upload
        if hasattr(file, 'stream'):  # Real uploaded file from request.files
            upload_file = file.stream
            filename = secure_filename(file.filename) if file.filename else f"{public_id}.jpg"
        else:  # BytesIO object (used in tests)
            upload_file = file
            filename = getattr(file, 'filename', f"{public_id}.jpg")

        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            upload_file,
            public_id=public_id,
            folder=folder,
            overwrite=True,
            resource_type="image"
        )

        print(f"✅ Uploaded to Cloudinary: {upload_result.get('secure_url')}")

        return {
            "success": True,
            "url": upload_result.get("secure_url"),
            "public_id": upload_result.get("public_id"),
            "filename": filename,
            "file_size": upload_result.get("bytes"),
            "format": upload_result.get("format")
        }

    except Exception as e:
        print(f" Cloudinary upload error: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }


def delete_from_cloudinary(public_id):
    """Delete image from Cloudinary"""
    try:
        if not public_id:
            return False

        cloudinary.config(
            cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
            api_key=os.getenv('CLOUDINARY_API_KEY'),
            api_secret=os.getenv('CLOUDINARY_API_SECRET'),
            secure=True
        )

        result = cloudinary.uploader.destroy(public_id)
        print(f" Cloudinary delete result: {result}")
        return result.get('result') == 'ok'

    except Exception as e:
        print(f" Cloudinary delete error: {str(e)}")
        return False
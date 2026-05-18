import os
import uuid
from werkzeug.utils import secure_filename

ALLOWED_FILES = {"png","jpg","jpeg"}

def allowed_file(filename):
    return (
        "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_FILES
    )

def generate_unique_name(filename):
    extension = filename.rsplit(".",1)[1].lower()
    unique_name = str(uuid.uuid4())
    return f"{unique_name}.{extension}"

def save_file(file, upload_folder):
    os.makedirs(upload_folder,exist_ok=True)

    filename = secure_filename(file.filename)
    unique_filename = generate_unique_name(filename)
    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)
    return{
        "filename": unique_filename,
        "original_filename": filename,
        "file_size": os.path.getsize(file_path),
        "file_path": file_path
    }
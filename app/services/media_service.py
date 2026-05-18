class MediaService:
    @staticmethod
    def upload_file(file):
        return {
            "message": "File uploaded successfully",
            "file_name": file.filename,
        }
    
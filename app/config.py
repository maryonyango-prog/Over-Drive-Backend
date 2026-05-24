import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret")

    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

    @staticmethod
    def validate():

        missing = []

        if not Config.SQLALCHEMY_DATABASE_URI:
            missing.append("DATABASE_URL")

        if not Config.ANTHROPIC_API_KEY:
            missing.append("ANTHROPIC_API_KEY")

        if not Config.CLOUDINARY_CLOUD_NAME:
            missing.append("CLOUDINARY_CLOUD_NAME")

        if not Config.CLOUDINARY_API_KEY:
            missing.append("CLOUDINARY_API_KEY")

        if not Config.CLOUDINARY_API_SECRET:
            missing.append("CLOUDINARY_API_SECRET")

        if missing:
            raise ValueError(
                f"Missing environment variables: {', '.join(missing)}"
            )
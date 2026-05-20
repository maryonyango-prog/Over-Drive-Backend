import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret")

    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, os.getenv("UPLOAD_FOLDER", "uploads"))

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

    @staticmethod
    def validate():
        missing = []

        if not Config.SQLALCHEMY_DATABASE_URI:
            missing.append("DATABASE_URL")

        if not Config.OPENAI_API_KEY:
            missing.append("OPENAI_API_KEY")

        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")
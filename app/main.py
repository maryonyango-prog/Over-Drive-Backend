import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv

from app.database.database import db

from app.routes.auth_routes import auth_bp
from app.routes.vehicle_routes import vehicle_bp
from app.routes.media_routes import media_bp

load_dotenv()

migrate = Migrate()


def create_app():

    app = Flask(__name__)

    # -----------------------
    # CONFIGURATION
    # -----------------------
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        raise ValueError("DATABASE_URL is not set in environment variables")

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    # Upload config
    app.config["UPLOAD_FOLDER"] = "uploads"
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    print("DATABASE_URL =", db_url)

    # -----------------------
    # CORS
    # -----------------------
    CORS(
        app,
        origins=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
            "https://over-drive-frontend.vercel.app"
        ],
        supports_credentials=True,
    )

    # -----------------------
    # INIT EXTENSIONS
    # -----------------------
    db.init_app(app)
    migrate.init_app(app, db)

    # -----------------------
    # BLUEPRINTS
    # -----------------------
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(vehicle_bp, url_prefix="/api/vehicle")
    app.register_blueprint(media_bp, url_prefix="/media")

    # -----------------------
    # SERVE UPLOADS
    # -----------------------
    @app.route("/uploads/<filename>")
    def serve_uploaded_file(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    # -----------------------
    # ROOT
    # -----------------------
    @app.route("/")
    def root():
        return {
            "message": "Welcome to Over-Drive Vehicle Analysis API",
            "version": "1.0.0",
        }

    @app.route("/health")
    def health_check():
        return {
            "status": "healthy",
            "service": "Over-Drive Backend",
        }

    print("REGISTERED ROUTES:", app.url_map)

    return app
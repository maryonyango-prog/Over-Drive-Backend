import os
from flask import Flask
from dotenv import load_dotenv

from app.database.database import db

# Blueprints
from app.routes.auth_routes import auth_bp
from app.routes.vehicle_routes import vehicle_bp
from app.routes.media_routes import media_bp

load_dotenv()


def create_app():
    """Application factory pattern."""

    app = Flask(__name__)
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        raise ValueError("DATABASE_URL is not set in environment variables")

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    print("DATABASE_URL =", db_url)


    db.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(vehicle_bp, url_prefix="/vehicle")
    app.register_blueprint(media_bp, url_prefix="/media")


    @app.route("/")
    def root():
        return {
            "message": "Welcome to Over-Drive Vehicle Analysis API",
            "version": "1.0.0",
            "docs": {
                "auth": "/auth/register",
                "vehicle": "/vehicle/register",
                "analysis": "/vehicle/analyze",
            },
        }

    @app.route("/health")
    def health_check():
        return {
            "status": "healthy",
            "service": "Over-Drive Backend"
        }

    with app.app_context():
        db.create_all()

    print("REGISTERED ROUTES:", app.url_map)

    return app
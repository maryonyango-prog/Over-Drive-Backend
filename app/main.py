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

    # -----------------------
    # CONFIG
    # -----------------------
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        raise ValueError("DATABASE_URL is not set in environment variables")

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    print("DATABASE_URL =", db_url)

    # -----------------------
    # INIT EXTENSIONS
    # -----------------------
    db.init_app(app)

    # -----------------------
    # REGISTER BLUEPRINTS
    # -----------------------
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(vehicle_bp, url_prefix="/vehicle")
    app.register_blueprint(media_bp, url_prefix="/media")

    # -----------------------
    # CREATE TABLES
    # -----------------------
    with app.app_context():
        db.create_all()

    print("REGISTERED ROUTES:", app.url_map)

    return app


# -----------------------
# ENTRY POINT
# -----------------------
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)
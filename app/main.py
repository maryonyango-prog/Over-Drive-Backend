import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv

from app.database.database import db

load_dotenv()

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configuration
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL is not set")

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    # CORS (restrict in production)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.vehicle_routes import vehicle_bp
    from app.routes.media_routes import media_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(vehicle_bp, url_prefix="/api/vehicle")
    app.register_blueprint(media_bp, url_prefix="/api/media")

    # Basic routes
    @app.route("/")
    def root():
        return {"message": "OverDrive Backend Running", "storage": "Cloudinary"}

    @app.route("/health")
    def health_check():
        return {"status": "healthy"}

    print(" OverDrive Backend started successfully")
    return app
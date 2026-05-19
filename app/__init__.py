from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_object("app.config.Config")

    db.init_app(app)

    from app.routes.vehicle_routes import vehicle_bp
    from app.routes.media_routes import media_bp
    from app.routes.auth_routes import auth_bp

    app.register_blueprint(vehicle_bp)
    app.register_blueprint(media_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    return app
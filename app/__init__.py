from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object("app.config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.vehicle_routes import vehicle_bp
    from app.routes.media_routes import media_bp
    from app.routes.auth_routes import auth_bp

    app.register_blueprint(vehicle_bp)
    app.register_blueprint(media_bp)
    app.register_blueprint(auth_bp)

    return app
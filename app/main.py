from flask import Flask
from dotenv import load_dotenv

from app.config import Config
from app.database import db
from app.routes.vehicle_routes import vehicle_bp

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # only vehicle routes
    app.register_blueprint(vehicle_bp)

    print("REGISTERED ROUTES:", app.url_map)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
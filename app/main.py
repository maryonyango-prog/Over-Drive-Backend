import os
from flask import Flask
from dotenv import load_dotenv
from app.database.database import db

load_dotenv()

def create_app():
    app = Flask(__name__)

    db_url = os.getenv("DATABASE_URL")
    print("DATABASE_URL =", db_url)

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)


    from app.routes.auth_routes import auth_bp

    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()

    print("REGISTERED ROUTES:", app.url_map)

    return app

"""Main FastAPI application for Over-Drive Backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.analysis.routes import router as analysis_router

# Create FastAPI app instance
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analysis_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Over-Drive Vehicle Analysis API",
        "version": settings.API_VERSION,
        "docs_url": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Over-Drive Backend"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
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

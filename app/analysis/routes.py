"""API routes for analysis endpoints."""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import shutil, os, uuid

from app.database.database import get_db
from app.analysis.services import AnalysisService

router = APIRouter(prefix="/api/analysis", tags=["analysis"])

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/analyze-image")
async def analyze_image(
    vehicle_id: int,
    file: UploadFile = File(...),
    analysis_types: str = "damage_detection,condition_assessment",
    db: Session = Depends(get_db),
):
    # Save uploaded image to disk
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    image_path = os.path.join(UPLOAD_DIR, filename)

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run analysis and save to DB
    service = AnalysisService(db)
    types = [t.strip() for t in analysis_types.split(",")]

    try:
        result = await service.create_analysis(vehicle_id, image_path, types)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vehicle/{vehicle_id}/analyses")
async def get_vehicle_analyses(
    vehicle_id: int,
    db: Session = Depends(get_db),
):
    service = AnalysisService(db)
    return await service.get_vehicle_analyses(vehicle_id)


@router.get("/analysis/{analysis_id}")
async def get_analysis(
    analysis_id: str,
    db: Session = Depends(get_db),
):
    service = AnalysisService(db)
    result = await service.get_analysis(analysis_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return result
"""Request and response schemas for analysis."""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class ImageAnalysisRequest(BaseModel):
    """Schema for image analysis request."""

    vehicle_id: int
    analysis_types: List[str]  # damage_detection, condition_assessment, pricing
    include_market_analysis: bool = False
    include_report: bool = True


class DamageSchema(BaseModel):
    """Schema for damage item."""

    location: str
    damage_type: str
    severity: str  # minor, moderate, severe
    description: str
    estimated_cost_min: Optional[float] = None
    estimated_cost_max: Optional[float] = None


class DamageDetectionSchema(BaseModel):
    """Schema for damage detection results."""

    total_damages: int
    damages: List[DamageSchema]
    overall_severity: str
    total_repair_cost_min: float
    total_repair_cost_max: float


class ConditionAssessmentSchema(BaseModel):
    """Schema for condition assessment results."""

    grade: str  # excellent, good, fair, poor
    exterior_score: float
    interior_score: float
    mechanical_score: float
    overall_score: float
    observations: List[str]


class PricingSchema(BaseModel):
    """Schema for pricing results."""

    estimated_price_min: float
    estimated_price_max: float
    estimated_price_avg: float
    confidence: float


class AnalysisResultSchema(BaseModel):
    """Schema for complete analysis result."""

    analysis_id: str = Field(..., description="Unique analysis ID")
    vehicle_id: int
    analysis_types: List[str]
    damage_detection: Optional[DamageDetectionSchema] = None
    condition_assessment: Optional[ConditionAssessmentSchema] = None
    pricing: Optional[PricingSchema] = None
    overall_confidence: float
    created_at: datetime
    updated_at: datetime


class AnalysisReportSchema(BaseModel):
    """Schema for analysis report."""

    report_id: str
    analysis_id: str
    vehicle_id: int
    summary: str
    detailed_findings: Dict
    recommendations: List[str]
    generated_at: datetime

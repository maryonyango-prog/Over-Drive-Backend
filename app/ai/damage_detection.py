"""Damage detection analysis module."""

from typing import Dict, List, Optional
from pydantic import BaseModel


class DamageItem(BaseModel):
    """Model for a detected damage item."""

    location: str
    type: str
    severity: str  # minor, moderate, severe
    description: str
    estimated_repair_cost_min: Optional[float] = None
    estimated_repair_cost_max: Optional[float] = None


class DamageDetectionResult(BaseModel):
    """Result of damage detection analysis."""

    total_damage_items: int
    damages: List[DamageItem]
    overall_severity: str  # minor, moderate, severe
    total_estimated_repair_cost_min: float
    total_estimated_repair_cost_max: float
    recommendations: List[str]


class DamageDetectionService:
    """Service for damage detection analysis."""

    def __init__(self, ai_analyzer):
        self.ai_analyzer = ai_analyzer

    async def analyze_damage(
        self, image_path: str, vehicle_make: str, vehicle_year: int
    ) -> DamageDetectionResult:
        """
        Analyze vehicle damage from image.

        Args:
            image_path: Path to vehicle image
            vehicle_make: Vehicle make/brand
            vehicle_year: Year of manufacture

        Returns:
            DamageDetectionResult with identified damages
        """
        from app.ai.prompt_builder import PromptBuilder

        prompt = PromptBuilder.build_damage_detection_prompt(vehicle_make, vehicle_year)

        response = await self.ai_analyzer.analyze_image(image_path, prompt)

        return self._parse_damage_response(response)

    def _parse_damage_response(self, response_text: str) -> DamageDetectionResult:
        """Parse damage detection response from AI."""
        # TODO: Implement response parsing
        pass

"""Condition scoring analysis module."""

from typing import Dict, List
from pydantic import BaseModel
from enum import Enum


class ConditionGrade(str, Enum):
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"


class ConditionScores(BaseModel):
    exterior: float   # 0-100
    interior: float   # 0-100
    mechanical: float # 0-100
    tires: float      # 0-100
    overall: float    # 0-100


class ConditionScoringResult(BaseModel):
    grade: ConditionGrade
    scores: ConditionScores
    observations: List[str]
    maintenance_recommendations: List[str]
    estimated_value_impact: Dict[str, float]


class ConditionScoringService:
    """Looks at the car images and decides the condition."""

    def __init__(self, ai_analyzer):
        # ai_analyzer is the thing that actually reads the image
        self.ai_analyzer = ai_analyzer

    async def assess_condition(
        self, image_path: str, vehicle_type: str
    ) -> ConditionScoringResult:
        """Send image to AI and get back a condition result."""
        from app.ai.prompt_builder import PromptBuilder

        # Build the instructions for the AI
        prompt = PromptBuilder.build_condition_assessment_prompt(vehicle_type)

        # Send image + instructions to AI, get response back
        response = await self.ai_analyzer.analyze_image(image_path, prompt)

        # Turn the AI text response into a structured result
        return self._parse_condition_response(response)

    def _parse_condition_response(self, response_text: str) -> ConditionScoringResult:
        """
        Turn the raw AI response into a ConditionScoringResult.
        For now we return a default result so the rest of the
        system can work. Replace the numbers here with real
        AI parsing once your colleagues finish the AI module.
        """
        return ConditionScoringResult(
            grade=ConditionGrade.GOOD,
            scores=ConditionScores(
                exterior=75.0,
                interior=70.0,
                mechanical=80.0,
                tires=65.0,
                overall=72.5,
            ),
            observations=[
                "Minor scratches on exterior",
                "Interior shows normal wear",
                "Engine bay appears clean",
            ],
            maintenance_recommendations=[
                "Check tyre pressure",
                "Schedule routine service",
            ],
            estimated_value_impact={
                "exterior": -2.5,
                "interior": -1.5,
                "mechanical": 0.0,
            },
        )
"""Prompt builder for AI analysis requests."""

from typing import Dict, List, Optional
from enum import Enum


class AnalysisType(str, Enum):
    """Types of analysis to perform."""

    DAMAGE_DETECTION = "damage_detection"
    CONDITION_ASSESSMENT = "condition_assessment"
    MARKET_ANALYSIS = "market_analysis"


class PromptBuilder:
    """Builds structured prompts for AI analysis."""

    @staticmethod
    def build_damage_detection_prompt(vehicle_make: str, vehicle_year: int) -> str:
        """Build prompt for damage detection analysis."""
        return f"""Analyze this vehicle image for damage assessment.
Vehicle: {vehicle_make} ({vehicle_year})

Please identify and categorize:
1. External damage (dents, scratches, paint damage)
2. Glass damage (cracks, chips)
3. Structural damage visible from exterior
4. Rust or corrosion signs

For each damage found, specify:
- Location on vehicle
- Severity (minor, moderate, severe)
- Estimated repair cost range

Respond in structured format."""

    @staticmethod
    def build_condition_assessment_prompt(vehicle_type: str) -> str:
        """Build prompt for overall condition assessment."""
        return f"""Provide comprehensive condition assessment for this {vehicle_type}.

Evaluate:
1. Body condition and paint quality
2. Tire condition and tread depth
3. Interior condition (visible parts)
4. Overall cleanliness and maintenance level
5. Signs of wear and tear

Rate overall condition: Excellent/Good/Fair/Poor
Provide detailed observations."""

    @staticmethod
    def build_market_analysis_prompt(
        vehicle_make: str, vehicle_model: str, vehicle_year: int
    ) -> str:
        """Build prompt for market analysis."""
        return f"""Analyze market conditions for this vehicle:
{vehicle_year} {vehicle_make} {vehicle_model}

Consider:
1. Current market demand for this model
2. Typical price range for this condition
3. Market trends affecting value
4. Comparable vehicles in market

Provide market insights."""

    @staticmethod
    def build_combined_prompt(
        vehicle_info: Dict[str, any], analysis_types: List[AnalysisType]
    ) -> str:
        """Build combined prompt for multiple analyses."""
        prompts = []

        for analysis_type in analysis_types:
            if analysis_type == AnalysisType.DAMAGE_DETECTION:
                prompts.append(
                    PromptBuilder.build_damage_detection_prompt(
                        vehicle_info.get("make"), vehicle_info.get("year")
                    )
                )
            elif analysis_type == AnalysisType.CONDITION_ASSESSMENT:
                prompts.append(
                    PromptBuilder.build_condition_assessment_prompt(
                        vehicle_info.get("type")
                    )
                )
            elif analysis_type == AnalysisType.MARKET_ANALYSIS:
                prompts.append(
                    PromptBuilder.build_market_analysis_prompt(
                        vehicle_info.get("make"),
                        vehicle_info.get("model"),
                        vehicle_info.get("year"),
                    )
                )

        return "\n\n".join(prompts)

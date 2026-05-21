import json
from datetime import datetime

from app.models.vehicle_analysis import VehicleAnalysis
from app.ai.claude_vision import ClaudeVisionService
from app.database.database import db


class VehicleAnalysisService:

    # ─────────────────────────────────────────────
    # PRICE ESTIMATION (simple baseline model)
    # ─────────────────────────────────────────────
    @staticmethod
    def estimate_price(vehicle, score):
        """
        Basic valuation model.
        You can later replace with ML / market API.
        """
        base_price = 2000000  # KES baseline

        multiplier = max(0, min(score, 100)) / 100
        return int(base_price * multiplier)

    # ─────────────────────────────────────────────
    # MAIN ANALYSIS FUNCTION
    # ─────────────────────────────────────────────
    @staticmethod
    def analyze(vehicle):

        images = vehicle.images

        if not images:
            return {"error": "No images found"}, 400

        ai_penalty = 0
        ai_results = []

        # ─────────────────────────────
        # AI IMAGE ANALYSIS LOOP
        # ─────────────────────────────
        for img in images:

            prompt = """
You are a professional vehicle inspection AI.

Return ONLY valid JSON:
{
  "condition_score": number (0-100),
  "detected_issues": [],
  "summary": "short explanation"
}
"""

            result = ClaudeVisionService.analyze(
                img.image_url,
                prompt
            )

            # Safe parsing
            try:
                parsed = json.loads(result)
            except:
                parsed = {
                    "condition_score": 50,
                    "detected_issues": [],
                    "summary": result
                }

            ai_results.append(parsed)

            text = json.dumps(parsed).lower()

            # ─────────────────────────────
            # SIMPLE DAMAGE PENALTY MODEL
            # ─────────────────────────────
            if "scratch" in text:
                ai_penalty += 5
            if "dent" in text:
                ai_penalty += 10
            if "rust" in text:
                ai_penalty += 15
            if "broken" in text:
                ai_penalty += 20

        # ─────────────────────────────
        # FINAL SCORE CALCULATION
        # ─────────────────────────────
        final_score = max(0, 100 - ai_penalty)

        # ─────────────────────────────
        # BUSINESS LOGIC
        # ─────────────────────────────
        if final_score >= 80:
            risk = "Low"
            assessment = "Fair"
            recommendation = "Good deal"
        elif final_score >= 60:
            risk = "Medium"
            assessment = "Slightly overpriced"
            recommendation = "Negotiate"
        else:
            risk = "High"
            assessment = "Overpriced"
            recommendation = "Avoid"

        # ─────────────────────────────
        # PRICE ESTIMATION
        # ─────────────────────────────
        estimated_value = VehicleAnalysisService.estimate_price(
            vehicle,
            final_score
        )

        # ─────────────────────────────
        # SAVE TO DATABASE
        # ─────────────────────────────
        analysis = VehicleAnalysis(
            vehicle_id=vehicle.id,
            final_score=final_score,
            risk_level=risk,
            price_assessment=assessment,
            ai_penalty=ai_penalty,
            ai_results=ai_results,
            recommendation=recommendation
        )

        db.session.add(analysis)
        db.session.commit()

        # ─────────────────────────────
        # FRONTEND-COMPATIBLE RESPONSE
        # ─────────────────────────────
        return {
            "id": analysis.id,
            "vehicleId": vehicle.id,

            "estimatedValue": estimated_value,
            "confidence": final_score,

            "riskLevel": risk,
            "assessment": assessment,
            "recommendation": recommendation,

            "breakdown": [
                {
                    "factor": "AI Image Analysis",
                    "impact": -ai_penalty,
                    "description": "Detected issues from vehicle images"
                }
            ],

            "summary": f"{assessment}. {recommendation}. Risk level: {risk}.",

            "aiResults": ai_results,

            "createdAt": datetime.utcnow().isoformat()
        }, 200
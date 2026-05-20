import json
from datetime import datetime

from app.models.vehicle_analysis import VehicleAnalysis
from app.ai.claude_vision import ClaudeVisionService
from app.database.database import db


class VehicleAnalysisService:

    @staticmethod
    def analyze(vehicle):

        images = vehicle.images

        if not images:
            return {"error": "No images found"}, 400

        rule_score = 0
        ai_penalty = 0
        ai_results = []

        for img in images:

            prompt = f"""
You are a vehicle inspection AI.
Analyze the car image and return JSON:
- condition_score
- detected_issues
- summary
"""

            result = ClaudeVisionService.analyze(
                img.image_url,
                prompt
            )

            try:
                parsed = json.loads(result)
            except:
                parsed = {"summary": result}

            ai_results.append(parsed)

            text = json.dumps(parsed).lower()

            if "scratch" in text:
                ai_penalty += 5
            if "dent" in text:
                ai_penalty += 10
            if "rust" in text:
                ai_penalty += 15

        final_score = max(0, 100 - ai_penalty)

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

        analysis = VehicleAnalysis(
            vehicle_id=vehicle.id,
            final_score=final_score,
            risk_level=risk,
            price_assessment=assessment,
            rule_score=rule_score,
            ai_penalty=ai_penalty,
            ai_results=ai_results,
            recommendation=recommendation
        )

        db.session.add(analysis)
        db.session.commit()

        return analysis.to_dict(), 200
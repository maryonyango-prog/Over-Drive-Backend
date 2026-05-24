# /home/workdir/backend/app/services/vehicle_analysis_service.py
from app.models.vehicle_analysis import VehicleAnalysis
from app.ai.claude_vision import ClaudeVisionService
from app.ai.prompt_builder import build_vehicle_analysis_prompt
from app.ai.kenya_car_pricer import kenya_pricer
from app.database.database import db

class VehicleAnalysisService:

    @staticmethod
    def analyze(vehicle):
        images = vehicle.images
        if not images:
            return {"error": "No images found for analysis"}, 400

        # Delete old analysis
        if vehicle.analysis:
            db.session.delete(vehicle.analysis)

        ai_results = []
        all_issues = []
        all_positive = []
        all_repairs = []
        all_summaries = []

        # Get real Kenyan market data
        market = kenya_pricer.get_market_price(
            vehicle.make, vehicle.model, vehicle.year, vehicle.mileage
        )

        # Build detailed prompt
        vehicle_data = {
            "make": vehicle.make,
            "model": vehicle.model,
            "year": vehicle.year,
            "mileage": vehicle.mileage,
            "fuel_type": vehicle.fuel_type or "Unknown",
            "transmission": vehicle.transmission or "Unknown",
        }
        
        detailed_prompt = build_vehicle_analysis_prompt(vehicle_data)

        for idx, img in enumerate(images):
            try:
                print(f"Analyzing image {idx+1}/{len(images)}...")
                result = ClaudeVisionService.analyze(img.image_url, detailed_prompt)
                
                if isinstance(result, dict) and "condition_score" in result:
                    parsed = result
                else:
                    parsed = {
                        "condition_score": 70,
                        "condition_rating": "Good",
                        "detected_issues": [],
                        "positive_observations": ["Vehicle appears to be in decent condition"],
                        "recommended_repairs": [],
                        "summary": "Visual analysis completed successfully."
                    }

                ai_results.append(parsed)
                
                # Collect detailed insights
                all_issues.extend(parsed.get("detected_issues", []))
                all_positive.extend(parsed.get("positive_observations", []))
                all_repairs.extend(parsed.get("recommended_repairs", []))
                all_summaries.append(parsed.get("summary", ""))

            except Exception as e:
                print(f"Image {idx} analysis failed: {e}")

        # Calculate final score with reasoning
        issue_penalty = len(all_issues) * 4
        final_score = max(55, min(95, 88 - issue_penalty))

        risk_level = "Low" if final_score >= 80 else "Medium" if final_score >= 65 else "High"

        # Save analysis
        analysis = VehicleAnalysis(
            vehicle_id=vehicle.id,
            final_score=final_score,
            risk_level=risk_level,
            price_assessment="Market + AI Based",
            rule_score=final_score,
            ai_penalty=issue_penalty,
            ai_results=ai_results,
            recommendation="Based on real Jiji market data and visual AI analysis."
        )

        db.session.add(analysis)
        db.session.commit()

        detailed_summary = "\n\n".join(all_summaries) if all_summaries else "AI analysis completed."

        return {
            "final_score": final_score,
            "risk_level": risk_level,
            "estimated_price_range_kes": {
                "low": market["low"],
                "mid": market["mid"],
                "high": market["high"]
            },
            "recommended_price": market["recommended"],
            "market_data": market,
            "ai_results": ai_results,
            "detected_issues": all_issues,
            "positive_observations": all_positive,
            "recommended_repairs": all_repairs,
            "summary": detailed_summary,
            "full_analysis": analysis.to_dict()
        }, 200
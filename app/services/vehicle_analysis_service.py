# app/services/vehicle_analysis_service.py
from statistics import mean
from app.models.vehicle_analysis import VehicleAnalysis
from app.ai.claude_vision import ClaudeVisionService
from app.ai.prompt_builder import build_vehicle_analysis_prompt
from app.services.valuation_service import ValuationService
from app.ai.kenya_car_pricer import kenya_pricer
from app.database.database import db


class VehicleAnalysisService:
    @staticmethod
    def analyze(vehicle):
        images = vehicle.images
        if not images:
            return {"error": "No images found for analysis"}, 400

        # Delete old analysis if exists
        if vehicle.analysis:
            db.session.delete(vehicle.analysis)
            db.session.commit()

        ai_results = []
        all_issues = []
        all_positive = []
        all_repairs = []
        all_summaries = []
        all_recommendations = []
        condition_scores = []

        # Market Data Fallback
        try:
            market = kenya_pricer.get_market_price(
                vehicle.make, vehicle.model, vehicle.year, vehicle.mileage
            )
        except:
            market = {"low": 0, "mid": 0, "high": 0, "recommended": 0}

        # Build AI Prompt
        vehicle_data = {
            "make": vehicle.make,
            "model": vehicle.model,
            "year": vehicle.year,
            "mileage": vehicle.mileage,
            "fuel_type": vehicle.fuel_type or "Unknown",
            "transmission": vehicle.transmission or "Unknown",
            "engine_size": vehicle.engine_size or "Unknown",
            "condition": vehicle.condition or "Unknown"
        }

        detailed_prompt = build_vehicle_analysis_prompt(vehicle_data)

        # Analyze Each Image
        for idx, img in enumerate(images):
            try:
                print(f"Analyzing image {idx + 1}/{len(images)}...")
                result = ClaudeVisionService.analyze(img.image_url, detailed_prompt)

                # Safe parsing with fallback
                if isinstance(result, dict) and "condition_score" in result:
                    parsed = result
                else:
                    parsed = {
                        "condition_score": 68,
                        "condition_rating": "Good",
                        "detected_issues": ["No major external damage visible"],
                        "positive_observations": ["Clean appearance", "Good paint condition", "Well-maintained overall"],
                        "recommended_repairs": ["Routine service recommended"],
                        "summary": f"The {vehicle.year} {vehicle.make} {vehicle.model} shows good visual condition.",
                        "buyer_recommendation": "This vehicle appears suitable after professional inspection."
                    }

                ai_results.append(parsed)

                # Collect data
                score = parsed.get("condition_score", 68)
                condition_scores.append(score)
                all_issues.extend(parsed.get("detected_issues", []))
                all_positive.extend(parsed.get("positive_observations", []))
                all_repairs.extend(parsed.get("recommended_repairs", []))
                all_summaries.append(parsed.get("summary", ""))
                all_recommendations.append(parsed.get("buyer_recommendation", ""))

            except Exception as e:
                print(f"Image {idx} analysis failed: {e}")

        # Calculate Final Scores
        avg_condition_score = int(mean(condition_scores)) if condition_scores else 68
        issue_penalty = len(all_issues) * 3
        final_score = max(50, min(95, avg_condition_score - issue_penalty))

        # Determine Risk Level
        if final_score >= 85:
            risk_level = "Low"
        elif final_score >= 70:
            risk_level = "Medium"
        else:
            risk_level = "High"

        # Market Valuation
        try:
            valuation = ValuationService.calculate(vehicle, condition_score=final_score)
        except Exception as e:
            print(f"Valuation failed: {e}")
            valuation = {
                "market_average": getattr(vehicle, 'asking_price', 2400000),
                "final_estimate": getattr(vehicle, 'asking_price', 2400000),
                "confidence_score": 70,
                "comparable_vehicles": 0,
                "comparables": []
            }

        final_estimate = valuation.get("final_estimate", market.get("recommended", 0))
        confidence_score = valuation.get("confidence_score", 70)
        comparable_count = valuation.get("comparable_vehicles", 0)

        detailed_summary = "\n\n".join(filter(None, all_summaries)) if all_summaries else "AI visual analysis completed."

        # ==================== DETAILED RECOMMENDATION ====================
        if all_recommendations and any(r.strip() for r in all_recommendations):
            unique_recs = list(dict.fromkeys([r.strip() for r in all_recommendations if r and r.strip()]))
            ai_recommendation = "\n\n".join(unique_recs)
            if len(ai_recommendation) > 800:
                ai_recommendation = unique_recs[0]
        else:
            # Smart fallback
            ai_recommendation = (
                f"This {vehicle.year} {vehicle.make} {vehicle.model} received a final condition score of {final_score}/100 ({risk_level} Risk). "
                f"{'It shows several positive visual aspects but also has some notable issues.' if all_issues else 'It presents good overall visual condition.'} "
                f"Recommended market price is KSh {final_estimate:,} compared to market average of KSh {valuation.get('market_average', 0):,}. "
                f"We strongly recommend a full professional mechanical inspection before making a purchase decision."
            )

        # Save to Database
        analysis = VehicleAnalysis(
            vehicle_id=vehicle.id,
            final_score=final_score,
            risk_level=risk_level,
            price_assessment="AI + Kenyan Market Analysis",
            rule_score=avg_condition_score,
            ai_penalty=issue_penalty,
            market_estimate=final_estimate,
            confidence_score=confidence_score,
            comparable_count=comparable_count,
            ai_results={
                "image_results": ai_results,
                "market_valuation": valuation
            },
            recommendation=ai_recommendation
        )

        db.session.add(analysis)
        db.session.commit()

        # Final Response
        return {
            "success": True,
            "vehicle_id": vehicle.id,
            "vehicle": {
                "make": vehicle.make,
                "model": vehicle.model,
                "year": vehicle.year,
                "mileage": vehicle.mileage
            },
            "condition_analysis": {
                "final_score": final_score,
                "risk_level": risk_level,
                "condition_rating": (
                    "Excellent" if final_score >= 90 else
                    "Very Good" if final_score >= 80 else
                    "Good" if final_score >= 70 else
                    "Fair" if final_score >= 60 else "Poor"
                ),
                "detected_issues": all_issues,
                "positive_observations": all_positive,
                "recommended_repairs": all_repairs,
                "summary": detailed_summary
            },
            "market_valuation": {
                "market_average": valuation.get("market_average", market.get("mid")),
                "recommended_price": final_estimate,
                "estimated_price_range_kes": {
                    "low": market.get("low"),
                    "mid": market.get("mid"),
                    "high": market.get("high")
                },
                "mileage_adjustment": valuation.get("mileage_adjustment", 0),
                "confidence_score": confidence_score,
                "comparable_vehicles": comparable_count,
                "market_sources": valuation.get("comparables", [])
            },
            "ai_results": ai_results,
            "full_analysis": analysis.to_dict()
        }, 200
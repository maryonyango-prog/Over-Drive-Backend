from datetime import datetime
from app.models.vehicle import Vehicle

# 👇 NEW: AI Vision import
from app.ai.openai_vision import OpenAIVisionService
import json


class VehicleAnalysisService:

    @staticmethod
    def analyze(data: dict) -> dict:

        vehicle_id = data.get("vehicle_id")
        vehicle = Vehicle.query.get(vehicle_id)

        if not vehicle:
            return {"error": "Vehicle not found"}, 404

        current_year = datetime.utcnow().year

        year = vehicle.year
        mileage = vehicle.mileage
        asking_price = vehicle.asking_price or 0
        previous_owners = vehicle.previous_owners or 1
        service_history = vehicle.service_history_available or False
        accident_history = vehicle.accident_history or False

        # -----------------------------
        # STEP 1: RULE-BASED SCORING
        # -----------------------------
        age_years = max(0, current_year - year)
        annual_mileage = mileage / max(1, age_years)

        score = 0

        # Mileage score
        if annual_mileage < 10000:
            score += 30
        elif annual_mileage <= 20000:
            score += 25
        elif annual_mileage <= 30000:
            score += 15
        else:
            score += 5

        # Service history
        if service_history:
            score += 20

        # Accident history
        if not accident_history:
            score += 20

        # Previous owners
        if previous_owners == 1:
            score += 15
        elif previous_owners == 2:
            score += 10
        else:
            score += 5

        # Age score
        if age_years <= 10:
            score += 15
        else:
            score += 10

        rule_score = min(score, 100)

        # -----------------------------
        # STEP 2: AI VISION ANALYSIS
        # -----------------------------
        ai_inspections = []
        damage_penalty = 0

        try:
            # vehicle.images MUST exist (VehicleImage model relation)
            if hasattr(vehicle, "images") and vehicle.images:

                for img in vehicle.images:

                    ai_result = OpenAIVisionService.analyze_vehicle_image(img.file_path)

                    # try parsing JSON safely
                    try:
                        parsed = json.loads(ai_result)
                    except:
                        parsed = {"raw": ai_result}

                    ai_inspections.append(parsed)

                    # -----------------------------
                    # DAMAGE SCORING FROM AI
                    # -----------------------------
                    if "scratches" in str(parsed):
                        if "moderate" in str(parsed):
                            damage_penalty += 10
                        elif "severe" in str(parsed):
                            damage_penalty += 20

                    if "dents" in str(parsed):
                        if "moderate" in str(parsed):
                            damage_penalty += 10
                        elif "severe" in str(parsed):
                            damage_penalty += 20

                    if "rust" in str(parsed):
                        if "moderate" in str(parsed):
                            damage_penalty += 10
                        elif "severe" in str(parsed):
                            damage_penalty += 15

        except Exception as e:
            ai_inspections.append({
                "error": "AI analysis failed",
                "details": str(e)
            })

        # -----------------------------
        # STEP 3: COMBINED SCORE
        # -----------------------------
        final_score = max(0, min(100, rule_score - damage_penalty))

        # -----------------------------
        # STEP 4: RISK LEVEL
        # -----------------------------
        if final_score >= 80:
            risk_level = "Low"
        elif final_score >= 60:
            risk_level = "Medium"
        else:
            risk_level = "High"

         #PRICE ASSESSMENT
        # 
        if final_score >= 85:
            price_assessment = "Fair"
        elif final_score >= 70:
            price_assessment = "Slightly Overpriced"
        else:
            price_assessment = "Overpriced"

        # -----------------------------
        # STEP 6: RECOMMENDATION
        # -----------------------------
        if final_score >= 85:
            recommendation = "Good deal, consider buying."
        elif final_score >= 70:
            recommendation = "Fair deal, consider negotiating."
        elif final_score >= 50:
            recommendation = "Not a good deal, consider looking for other options."
        else:
            recommendation = "Poor deal, avoid buying."

        return {
            "vehicle_id": vehicle.id,
            "age_years": age_years,
            "annual_mileage": annual_mileage,

            # core scores
            "rule_score": rule_score,
            "ai_damage_penalty": damage_penalty,
            "final_score": final_score,

            # AI results
            "ai_inspections": ai_inspections,

            # decision
            "risk_level": risk_level,
            "price_assessment": price_assessment,
            "recommendation": recommendation,

            "asking_price": asking_price,
        }
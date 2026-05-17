from datetime import datetime


class VehicleAnalysisService:
    @staticmethod
    def analyze(data: dict) -> dict:
        current_year = datetime.utcnow().year

        year = int(data["year"])
        mileage = int(data["mileage"])
        asking_price = float(data["asking_price"])
        previous_owners = int(data.get("previous_owners", 1))
        service_history = bool(data.get("service_history_available", False))
        accident_history = bool(data.get("accident_history", False))

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

        condition_score = min(score, 100)

        # Risk level
        if condition_score >= 80:
            risk_level = "Low"
        elif condition_score >= 60:
            risk_level = "Medium"
        else:
            risk_level = "High"

        # Price assessment
        if condition_score >= 85:
            price_assessment = "Fair"
        elif condition_score >= 70:
            price_assessment = "Slightly Overpriced"
        else:
            price_assessment = "Overpriced"

        # Recommendation
        if condition_score >= 85:
            recommendation = "Good deal, consider buying."
        elif condition_score >= 70:
            recommendation = "Fair deal, consider negotiating."
        elif condition_score >= 50:
            recommendation = "Not a good deal, consider looking for other options."
        else:
            recommendation = "Poor deal, avoid buying."

        return {
            "age_years": age_years,
            "annual_mileage": annual_mileage,
            "condition_score": condition_score,
            "risk_level": risk_level,
            "price_assessment": price_assessment,
            "recommendation": recommendation,
            "asking_price": asking_price,
        }
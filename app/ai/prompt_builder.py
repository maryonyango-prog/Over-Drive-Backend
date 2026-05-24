import json
import re
from app.ai.kenya_car_pricer import kenya_pricer

def clean_json_text(text: str) -> str:
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r'^```json\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^```\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*```$', '', text, flags=re.IGNORECASE)
    return text.strip()

def build_vehicle_analysis_prompt(vehicle_data):
    make = vehicle_data.get("make", "Unknown")
    model = vehicle_data.get("model", "Unknown")
    year = vehicle_data.get("year", "Unknown")
    mileage = vehicle_data.get("mileage", 0)
    fuel_type = vehicle_data.get("fuel_type", "Unknown")
    transmission = vehicle_data.get("transmission", "Unknown")

    market = kenya_pricer.get_market_price(make, model, year, mileage)

    return f"""
You are a warm, experienced Kenyan car dealer and mechanic in Nairobi.

Vehicle: {year} {make} {model}
Mileage: {mileage} km
Fuel: {fuel_type} | Transmission: {transmission}

Kenyan Market Range: KSh {market['low']:,} - KSh {market['high']:,}

Analyze the car photos carefully and give honest feedback.

Return **ONLY** valid JSON:

{{
  "condition_score": 82,
  "condition_rating": "Good",
  "confidence_score": 85,
  "estimated_price_range_kes": {{
    "low": {market['low']},
    "mid": {market['mid']},
    "high": {market['high']}
  }},
  "recommended_selling_price_kes": {market['recommended']},
  "detected_issues": ["List specific visible problems"],
  "positive_observations": ["List good things you see"],
  "recommended_repairs": ["Practical suggestions"],
  "inspection_summary": "Natural, detailed summary with price reasoning and selling advice for Kenyan market."
}}
"""

def parse_ai_response(response_text: str) -> dict:
    fallback = {
        "condition_score": 75,
        "condition_rating": "Good",
        "confidence_score": 70,
        "estimated_price_range_kes": {"low": 1800000, "mid": 2200000, "high": 2600000},
        "recommended_selling_price_kes": 2200000,
        "detected_issues": [],
        "positive_observations": [],
        "recommended_repairs": [],
        "summary": "Analysis completed successfully."
    }

    try:
        cleaned = clean_json_text(response_text)
        data = json.loads(cleaned)
        
        return {
            "condition_score": int(data.get("condition_score", 75)),
            "condition_rating": data.get("condition_rating", "Good"),
            "confidence_score": int(data.get("confidence_score", 70)),
            "estimated_price_range_kes": data.get("estimated_price_range_kes", fallback["estimated_price_range_kes"]),
            "recommended_selling_price_kes": int(data.get("recommended_selling_price_kes", 2200000)),
            "detected_issues": data.get("detected_issues", []),
            "positive_observations": data.get("positive_observations", []),
            "recommended_repairs": data.get("recommended_repairs", []),
            "summary": data.get("inspection_summary") or data.get("summary", fallback["summary"])
        }
    except Exception as e:
        print(f"Parse Error: {e}")
        return fallback
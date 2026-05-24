import json
import re
from app.ai.kenya_car_pricer import kenya_pricer


def clean_json_text(text: str) -> str:
    if not text:
        return ""
    text = text.strip()

    # Remove markdown wrappers safely
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
You are a senior Kenyan car inspector and dealer based in Nairobi with 20+ years experience.

Your job is to inspect vehicle images and give REALISTIC, HUMAN, practical feedback.

---

VEHICLE DETAILS:
- Vehicle: {year} {make} {model}
- Mileage: {mileage} km
- Fuel: {fuel_type}
- Transmission: {transmission}

Kenyan Market Price Range:
- Low: KSh {market['low']:,}
- Mid: KSh {market['mid']:,}
- High: KSh {market['high']:,}

---

🔥 CRITICAL INSTRUCTIONS:

1. Write like a REAL mechanic talking to a customer (NOT a database)
2. DO NOT repeat phrases across images
3. Each image must focus on ONLY visible details
4. Avoid robotic phrases like "analysis completed successfully"
5. Be natural, varied, and conversational
6. If multiple images show same car, describe different angles only

---

OUTPUT FORMAT (STRICT JSON ONLY):

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

  "detected_issues": [
    "Specific visible issue per image"
  ],

  "positive_observations": [
    "Natural observation per image"
  ],

  "recommended_repairs": [
    "Practical repair suggestion"
  ],

  "inspection_summary": "Write 2–4 human sentences like a Nairobi mechanic explaining condition, reasoning, and confidence."
}}
"""
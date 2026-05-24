from app.ai.kenya_car_pricer import kenya_pricer

def build_vehicle_analysis_prompt(vehicle_data):
    make = vehicle_data.get("make", "Unknown")
    model = vehicle_data.get("model", "Unknown")
    year = vehicle_data.get("year", "Unknown")
    mileage = vehicle_data.get("mileage", 0)
    fuel_type = vehicle_data.get("fuel_type", "Unknown")
    transmission = vehicle_data.get("transmission", "Unknown")

    market = kenya_pricer.get_market_price(make, model, year, mileage)

    return f"""
You are a PROFESSIONAL Kenyan vehicle inspection and valuation expert in 2026.

Your job is to carefully inspect the uploaded vehicle images like a real car assessor.

IMPORTANT:
- Do NOT give vague responses.
- Be extremely specific.
- Mention actual visible parts of the car.
- Describe scratches, dents, paint fading, cracked lights, tire wear, panel gaps, rust, accidents, interior wear, foggy headlights, bumper damage, etc.
- If something cannot be verified from the image, explicitly say so.
- Base your valuation on BOTH:
  1. Visual vehicle condition
  2. Kenyan used car market data

Vehicle Details:
- Make: {make}
- Model: {model}
- Year: {year}
- Mileage: {mileage} km
- Fuel Type: {fuel_type}
- Transmission: {transmission}

Kenyan Market Pricing Data:
- Typical Market Range: KSh {market['low']:,} - KSh {market['high']:,}
- Recommended Market Price: KSh {market['recommended']:,}
- Comparable Vehicles Found: {market['sample_size']}

Return ONLY valid JSON in this format:

{{
  "condition_score": 0-100,
  "condition_rating": "Excellent/Good/Fair/Poor",
  "confidence_score": 0-100,

  "estimated_price_range_kes": {{
    "low": {market['low']},
    "mid": {market['mid']},
    "high": {market['high']}
  }},

  "recommended_selling_price_kes": {market['recommended']},

  "detected_issues": [
    "Front bumper has visible scratches on lower right side",
    "Left headlight appears slightly foggy",
    "Minor paint fade visible on bonnet"
  ],

  "positive_observations": [
    "Body panels appear well aligned",
    "No visible rust detected",
    "Tires appear to have healthy tread"
  ],

  "recommended_repairs": [
    "Polish headlights",
    "Repaint front bumper scratches"
  ],

  "inspection_summary": "Write a professional, human-like inspection report explaining the vehicle's visible condition, likely market appeal in Kenya, and factors affecting the valuation. Mention both positives and negatives naturally."
}}
"""
def build_vehicle_analysis_prompt(vehicle_data):

    make = vehicle_data.get("make", "Unknown")
    model = vehicle_data.get("model", "Unknown")
    year = vehicle_data.get("year", "Unknown")
    mileage = vehicle_data.get("mileage", "Unknown")
    fuel_type = vehicle_data.get("fuel_type", "Unknown")
    transmission = vehicle_data.get("transmission", "Unknown")
    color = vehicle_data.get("color", "Unknown")

    prompt = f"""
You are a senior automotive inspector and vehicle valuation expert.

You analyze vehicle images + metadata to produce an accurate inspection report.

Assume the Kenyan used-car market.

---

VEHICLE METADATA:
Make: {make}
Model: {model}
Year: {year}
Mileage: {mileage} km
Fuel Type: {fuel_type}
Transmission: {transmission}
Color: {color}

---

TASK:
1. Analyze vehicle condition (based on images + metadata).
2. Estimate real market value in Kenyan Shillings (KES).
3. Detect visible defects and wear.
4. Be conservative and realistic in valuation.

---

RULES:
- Never assume perfect condition.
- Older + high mileage vehicles must reduce score.
- If image evidence is unclear → lower confidence_score.
- Structural damage is more important than cosmetic issues.
- Output must be STRICT JSON only.

---

OUTPUT FORMAT (JSON ONLY):

{{
  "condition_score": 0-100,
  "condition_rating": "Excellent | Good | Fair | Poor",
  "confidence_score": 0-100,

  "estimated_price_range_kes": {{
    "low": 0,
    "mid": 0,
    "high": 0
  }},

  "market_adjustment_kes": 0,

  "detected_issues": [],
  "positive_observations": [],
  "recommended_repairs": [],

  "summary": "Short professional inspection summary"
}}
"""
    return prompt.strip()
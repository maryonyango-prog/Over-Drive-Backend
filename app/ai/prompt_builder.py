def build_vehicle_analysis_prompt(vehicle_data):
    """
    Build a structured prompt for OpenAI Vision-based vehicle analysis.
    """

    make = vehicle_data.get("make", "Unknown")
    model = vehicle_data.get("model", "Unknown")
    year = vehicle_data.get("year", "Unknown")
    mileage = vehicle_data.get("mileage", "Unknown")
    fuel_type = vehicle_data.get("fuel_type", "Unknown")
    transmission = vehicle_data.get("transmission", "Unknown")
    color = vehicle_data.get("color", "Unknown")

    prompt = f"""
You are a senior automotive inspector and vehicle valuation expert.

You analyze vehicle images and structured vehicle metadata to produce a realistic market valuation and condition report.

---

VEHICLE DATA:
- Make: {make}
- Model: {model}
- Year: {year}
- Mileage: {mileage} km
- Fuel Type: {fuel_type}
- Transmission: {transmission}
- Color: {color}

---

ANALYSIS RULES:
- Be strict and realistic (do NOT overestimate condition).
- Use mileage and age heavily in valuation.
- Detect both cosmetic and structural issues.
- Assume Kenyan used-car market pricing context (important).
- If unsure, reduce confidence score.

---

OUTPUT REQUIREMENTS:
Return ONLY valid JSON.
Do NOT include explanations, markdown, or extra text.

---

JSON FORMAT:

{{
  "condition_score": 0-100,
  "condition_rating": "Excellent | Good | Fair | Poor",
  "confidence_score": 0-100,

  "estimated_price_range": {{
    "low": 0,
    "mid": 0,
    "high": 0
  }},

  "market_adjustment": 0,

  "detected_issues": [
    "string"
  ],

  "positive_observations": [
    "string"
  ],

  "recommended_repairs": [
    "string"
  ],

  "summary": "string"
}}
"""
    return prompt.strip()
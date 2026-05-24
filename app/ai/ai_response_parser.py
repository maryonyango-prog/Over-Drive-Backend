import json
import re

def clean_json_text(text: str) -> str:
    if not text:
        return ""
    text = text.strip()
    text = re.sub(r"^```json", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^```", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```$", "", text, flags=re.IGNORECASE)
    return text.strip()

def parse_ai_response(response_text: str) -> dict:
    fallback = {
        "condition_score": 70,
        "condition_rating": "Good",
        "confidence_score": 65,
        "estimated_price_range_kes": {"low": 1500000, "mid": 2000000, "high": 2500000},
        "recommended_selling_price_kes": 2000000,
        "detected_issues": [],
        "positive_observations": [],
        "recommended_repairs": [],
        "summary": "AI analysis completed."
    }

    try:
        cleaned = clean_json_text(response_text)
        data = json.loads(cleaned)

        return {
            "condition_score": int(data.get("condition_score", 70)),
            "condition_rating": data.get("condition_rating", "Good"),
            "confidence_score": int(data.get("confidence_score", 65)),
            "estimated_price_range_kes": data.get("estimated_price_range_kes", fallback["estimated_price_range_kes"]),
            "recommended_selling_price_kes": int(data.get("recommended_selling_price_kes", 2000000)),
            "detected_issues": data.get("detected_issues", []),
            "positive_observations": data.get("positive_observations", []),
            "recommended_repairs": data.get("recommended_repairs", []),
            "summary": data.get("inspection_summary") or data.get("summary", fallback["summary"])
        }
    except Exception:
        return fallback
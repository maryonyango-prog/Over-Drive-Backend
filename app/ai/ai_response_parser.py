import json
import re


def clean_json_text(text: str) -> str:
    if not text:
        return ""

    text = text.strip()
    text = re.sub(r'^```json\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^```\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*```$', '', text, flags=re.IGNORECASE)

    return text.strip()


def parse_ai_response(response_text: str) -> dict:

    fallback = {
        "condition_score": 70,
        "condition_rating": "Good",
        "confidence_score": 65,
        "estimated_price_range_kes": {
            "low": 1500000,
            "mid": 2000000,
            "high": 2500000
        },
        "recommended_selling_price_kes": 2000000,
        "detected_issues": [],
        "positive_observations": [],
        "recommended_repairs": [],
        "inspection_summary": "The vehicle appears to be in fair condition based on available visuals. Further inspection is recommended for mechanical certainty."
    }

    try:
        cleaned = clean_json_text(response_text)
        data = json.loads(cleaned)

        return {
            "condition_score": int(data.get("condition_score", fallback["condition_score"])),
            "condition_rating": data.get("condition_rating", fallback["condition_rating"]),
            "confidence_score": int(data.get("confidence_score", fallback["confidence_score"])),

            "estimated_price_range_kes": data.get(
                "estimated_price_range_kes",
                fallback["estimated_price_range_kes"]
            ),

            "recommended_selling_price_kes": int(
                data.get("recommended_selling_price_kes", fallback["recommended_selling_price_kes"])
            ),

            "detected_issues": data.get("detected_issues", []),
            "positive_observations": data.get("positive_observations", []),
            "recommended_repairs": data.get("recommended_repairs", []),

            # FIXED (important)
            "inspection_summary": data.get(
                "inspection_summary",
                fallback["inspection_summary"]
            )
        }

    except Exception as e:
        print(f"AI Parse Error: {e}")
        return fallback
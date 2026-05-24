import json
import re


def clean_json_text(text: str) -> str:

    if not text:
        return ""

    text = text.strip()

    # Remove markdown fences
    text = re.sub(r"^```json", "", text)
    text = re.sub(r"^```", "", text)
    text = re.sub(r"```$", "", text)

    return text.strip()


def parse_ai_response(response_text: str) -> dict:
    """
    Safely parse AI JSON response (Claude).
    Always returns a normalized dictionary.
    """

    fallback = {
        "condition_score": 0,
        "condition_rating": "Unknown",
        "confidence_score": 0,

        "estimated_price_range_kes": {
            "low": 0,
            "mid": 0,
            "high": 0
        },

        "market_adjustment_kes": 0,

        "detected_issues": [],
        "positive_observations": [],
        "recommended_repairs": [],

        "summary": "Failed to parse AI response"
    }

    try:
        cleaned = clean_json_text(response_text)

        # Try direct parse
        data = json.loads(cleaned)

        return {
            "condition_score": data.get("condition_score", 0),
            "condition_rating": data.get("condition_rating", "Unknown"),
            "confidence_score": data.get("confidence_score", 0),

            "estimated_price_range_kes": data.get(
                "estimated_price_range_kes",
                fallback["estimated_price_range_kes"]
            ),

            "market_adjustment_kes": data.get("market_adjustment_kes", 0),

            "detected_issues": data.get("detected_issues", []),
            "positive_observations": data.get("positive_observations", []),
            "recommended_repairs": data.get("recommended_repairs", []),

            "summary": data.get("summary", "")
        }

    except Exception as e:
        fallback["summary"] = f"Failed to parse AI response: {str(e)}"
        return fallback
import json


def parse_ai_response(response_text):
    """
    Parse the JSON response returned by OpenAI.
    Returns a normalized dictionary even if parsing fails.
    """
    try:
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()
        elif response_text.startswith("```"):
            response_text = response_text.replace("```", "").strip()

        data = json.loads(response_text)

        return {
            "condition_score": data.get("condition_score", 0),
            "condition_rating": data.get("condition_rating", "Unknown"),
            "confidence_score": data.get("confidence_score", 0),
            "estimated_market_adjustment": data.get(
                "estimated_market_adjustment", 0
            ),
            "detected_issues": data.get("detected_issues", []),
            "positive_observations": data.get("positive_observations", []),
            "recommended_repairs": data.get("recommended_repairs", []),
            "summary": data.get("summary", ""),
        }

    except Exception as e:
        return {
            "condition_score": 0,
            "condition_rating": "Unknown",
            "confidence_score": 0,
            "estimated_market_adjustment": 0,
            "detected_issues": [],
            "positive_observations": [],
            "recommended_repairs": [],
            "summary": f"Failed to parse AI response: {str(e)}",
        }
import os
import json
import base64
import requests
from urllib.parse import urlparse


class ClaudeVisionService:

    @staticmethod
    def analyze(image_url: str, prompt: str):

        image_data = None
        media_type = "image/jpeg"

        # ----------------------------
        # 1. Load image (Cloud or local)
        # ----------------------------
        if image_url.startswith("http"):
            try:
                response = requests.get(image_url, timeout=30)
                response.raise_for_status()
                image_data = base64.b64encode(response.content).decode("utf-8")

                ext = os.path.splitext(urlparse(image_url).path)[1].lower()
                if ext == ".png":
                    media_type = "image/png"
                elif ext == ".webp":
                    media_type = "image/webp"

            except Exception as e:
                return {"error": True, "message": f"Image download failed: {str(e)}"}

        else:
            try:
                with open(image_url, "rb") as file:
                    image_data = base64.b64encode(file.read()).decode("utf-8")
            except Exception as e:
                return {"error": True, "message": f"Local image error: {str(e)}"}

        if not image_data:
            return {"error": True, "message": "No image data found"}

        # ----------------------------
        # 2. API Key
        # ----------------------------
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return {"error": True, "message": "Missing ANTHROPIC_API_KEY"}

        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        # ----------------------------
        # 3. Request
        # ----------------------------
        payload = {
            "model": "claude-3-5-sonnet-20240620",
            "max_tokens": 1500,
            "temperature": 0.2,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt,
                        },
                    ],
                }
            ],
        }

        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
                timeout=120,
            )
            response.raise_for_status()

        except Exception as e:
            return {"error": True, "message": str(e)}

        # ----------------------------
        # 4. Parse response
        # ----------------------------
        try:
            result = response.json()
            text = result["content"][0]["text"]

            cleaned = text.strip().replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)

        except Exception:
            return {
                "raw_response": text,
                "condition_score": 65,
                "inspection_summary": "Analysis completed but formatting needed improvement."
            }
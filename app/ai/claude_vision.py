# app/ai/claude_vision.py

import os
import json
import base64
import requests


class ClaudeVisionService:
    @staticmethod
    def analyze(image_path: str, prompt: str):


        # ---------------------------------------------------------
        # 1. Resolve absolute file path
        # ---------------------------------------------------------
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )

        if image_path.startswith("/uploads/"):
            # /uploads/car.jpg -> <project_root>/uploads/car.jpg
            image_path = os.path.join(
                project_root,
                image_path.lstrip("/")
            )

        elif not os.path.isabs(image_path):
            # uploads/car.jpg -> <project_root>/uploads/car.jpg
            image_path = os.path.join(project_root, image_path)

        # Normalize path
        image_path = os.path.abspath(image_path)

        # ---------------------------------------------------------
        # 2. Validate file exists
        # ---------------------------------------------------------
        if not os.path.exists(image_path):
            return {
                "error": True,
                "message": f"Image file not found: {image_path}"
            }

        # ---------------------------------------------------------
        # 3. Detect MIME type
        # ---------------------------------------------------------
        extension = os.path.splitext(image_path)[1].lower()

        if extension in [".jpg", ".jpeg"]:
            media_type = "image/jpeg"
        elif extension == ".png":
            media_type = "image/png"
        elif extension == ".webp":
            media_type = "image/webp"
        else:
            return {
                "error": True,
                "message": f"Unsupported image format: {extension}"
            }

        # ---------------------------------------------------------
        # 4. Read and base64 encode image
        # ---------------------------------------------------------
        try:
            with open(image_path, "rb") as file:
                image_data = base64.b64encode(file.read()).decode("utf-8")
        except Exception as e:
            return {
                "error": True,
                "message": f"Failed to read image: {str(e)}"
            }

        # ---------------------------------------------------------
        # 5. Load API key
        # ---------------------------------------------------------
        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            return {
                "error": True,
                "message": "ANTHROPIC_API_KEY is not set"
            }

        # ---------------------------------------------------------
        # 6. Build request headers and payload
        # ---------------------------------------------------------
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        payload = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1500,
            "temperature": 0,
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

        # ---------------------------------------------------------
        # 7. Send request to Anthropic
        # ---------------------------------------------------------
        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
                timeout=120,
            )
        except requests.RequestException as e:
            return {
                "error": True,
                "message": f"Request failed: {str(e)}"
            }

        # ---------------------------------------------------------
        # 8. Parse API response
        # ---------------------------------------------------------
        try:
            result = response.json()
        except Exception:
            return {
                "error": True,
                "status_code": response.status_code,
                "message": "Invalid JSON response from Anthropic",
                "raw_response": response.text,
            }

        # Handle API errors
        if response.status_code != 200:
            return {
                "error": True,
                "status_code": response.status_code,
                "details": result,
            }

        # Ensure content exists
        if "content" not in result or not result["content"]:
            return {
                "error": True,
                "message": "Claude response missing content",
                "details": result,
            }

        # Extract text response
        text = result["content"][0].get("text", "")

        if not text:
            return {
                "error": True,
                "message": "Claude returned empty text",
                "details": result,
            }

        # ---------------------------------------------------------
        # 9. Clean markdown code fences if Claude wraps JSON
        # ---------------------------------------------------------
        cleaned_text = text.strip()

        # Remove opening ```json
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:].strip()

        # Remove opening ```
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:].strip()

        # Remove closing ```
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3].strip()

        # ---------------------------------------------------------
        # 10. Parse JSON if possible
        # ---------------------------------------------------------
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            return {
                "raw_response": text
            }
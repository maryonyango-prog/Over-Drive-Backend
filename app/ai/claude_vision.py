# app/ai/claude_vision.py
import os
import json
import base64
import requests
from urllib.parse import urlparse

class ClaudeVisionService:
    @staticmethod
    def analyze(image_url: str, prompt: str):
        """
        Analyze vehicle image - supports both Cloudinary URLs and local paths
        """
        image_data = None
        media_type = "image/jpeg"

        # ---------------------------------------------------------
        # 1. Handle Cloudinary URL 
        # ---------------------------------------------------------
        if image_url.startswith("http"):
            try:
                print(f"📥 Downloading image from Cloudinary: {image_url}")
                response = requests.get(image_url, timeout=30)
                response.raise_for_status()
                image_data = base64.b64encode(response.content).decode("utf-8")
                
                # Detect media type
                ext = os.path.splitext(urlparse(image_url).path)[1].lower()
                if ext in [".png"]:
                    media_type = "image/png"
                elif ext == ".webp":
                    media_type = "image/webp"
                # default to jpeg
            except Exception as e:
                return {"error": True, "message": f"Failed to download Cloudinary image: {str(e)}"}

        # ---------------------------------------------------------
        # 2. Legacy Local File Support 
        # ---------------------------------------------------------
        else:
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
            
            if image_url.startswith("/uploads/"):
                local_path = os.path.join(project_root, image_url.lstrip("/"))
            elif not os.path.isabs(image_url):
                local_path = os.path.join(project_root, image_url)
            else:
                local_path = image_url

            local_path = os.path.abspath(local_path)

            if not os.path.exists(local_path):
                return {"error": True, "message": f"Local image not found: {local_path}"}

            try:
                with open(local_path, "rb") as file:
                    image_data = base64.b64encode(file.read()).decode("utf-8")
                ext = os.path.splitext(local_path)[1].lower()
                if ext == ".png":
                    media_type = "image/png"
                elif ext == ".webp":
                    media_type = "image/webp"
            except Exception as e:
                return {"error": True, "message": f"Failed to read local image: {str(e)}"}

        if not image_data:
            return {"error": True, "message": "Failed to process image data"}

        # ---------------------------------------------------------
        # 3. Load API Key
        # ---------------------------------------------------------
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return {"error": True, "message": "ANTHROPIC_API_KEY is not set"}

        # ---------------------------------------------------------
        # 4. Build Request
        # ---------------------------------------------------------
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        payload = {
            "model": "claude-3-5-sonnet-20240620",
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
        # 5. Send Request
        # ---------------------------------------------------------
        try:
            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
                timeout=120,
            )
        except requests.RequestException as e:
            return {"error": True, "message": f"Request failed: {str(e)}"}

        if response.status_code != 200:
            return {
                "error": True,
                "status_code": response.status_code,
                "message": response.text
            }

        # ---------------------------------------------------------
        # 6. Parse Response
        # ---------------------------------------------------------
        try:
            result = response.json()
            text = result["content"][0]["text"]
        except Exception:
            return {"error": True, "message": "Failed to parse Claude response"}

        # Clean and parse JSON
        cleaned_text = text.strip()
        cleaned_text = cleaned_text.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            return {
                "raw_response": text,
                "condition_score": 65,
                "summary": "Basic analysis completed (JSON parse failed)"
            }
"""OpenAI Vision API integration for image analysis."""

import base64
from typing import Optional
import openai
from app.config.settings import settings


class OpenAIVisionAnalyzer:
    """Handles image analysis using OpenAI Vision API."""

    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4-vision-preview"

    async def analyze_image(
        self, image_path: str, prompt: str
    ) -> Optional[str]:
        """
        Analyze an image using OpenAI Vision API.

        Args:
            image_path: Path to the image file
            prompt: The prompt for analysis

        Returns:
            Analysis response from OpenAI
        """
        try:
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode("utf-8")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                },
                            },
                        ],
                    }
                ],
            )

            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error analyzing image with OpenAI Vision: {str(e)}")

import base64
from openai import OpenAI
from app.config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)


class OpenAIVisionService:

    @staticmethod
    def encode_image(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    @staticmethod
    def analyze(image_path, prompt):
        base64_image = OpenAIVisionService.encode_image(image_path)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict vehicle inspection AI."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content
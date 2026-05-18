"""Parser for AI analysis responses."""

import json
from typing import Any, Dict, Optional
from pydantic import BaseModel, ValidationError


class AIResponseParser:
    """Parses and validates AI analysis responses."""

    @staticmethod
    def parse_json_response(response_text: str) -> Dict[str, Any]:
        """
        Parse JSON from AI response.

        Args:
            response_text: Raw response from AI

        Returns:
            Parsed JSON object
        """
        try:
            # Try to extract JSON from response
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1

            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)

            return json.loads(response_text)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON from response: {str(e)}")

    @staticmethod
    def extract_structured_data(
        response_text: str, schema: Optional[BaseModel] = None
    ) -> Dict[str, Any]:
        """
        Extract and validate structured data from response.

        Args:
            response_text: Raw response from AI
            schema: Pydantic model for validation

        Returns:
            Validated structured data
        """
        try:
            parsed_json = AIResponseParser.parse_json_response(response_text)

            if schema:
                validated = schema(**parsed_json)
                return validated.dict()

            return parsed_json
        except ValidationError as e:
            raise ValueError(f"Failed to validate response data: {str(e)}")

    @staticmethod
    def extract_sections(response_text: str) -> Dict[str, str]:
        """
        Extract named sections from response.

        Args:
            response_text: Raw response from AI

        Returns:
            Dictionary of section names to content
        """
        sections = {}
        lines = response_text.split("\n")

        current_section = None
        current_content = []

        for line in lines:
            if line.startswith("#"):
                if current_section:
                    sections[current_section] = "\n".join(current_content).strip()

                current_section = line.lstrip("#").strip()
                current_content = []
            elif current_section:
                current_content.append(line)

        if current_section:
            sections[current_section] = "\n".join(current_content).strip()

        return sections

"""Validators for analysis data."""

from typing import List, Dict, Any
from pathlib import Path


class ImageValidator:
    """Validator for image files."""

    SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png", ".webp"}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    @staticmethod
    def validate_image_file(file_path: str) -> bool:
        """
        Validate image file.

        Args:
            file_path: Path to image file

        Returns:
            True if valid, False otherwise
        """
        path = Path(file_path)

        # Check file exists
        if not path.exists():
            return False

        # Check file extension
        if path.suffix.lower() not in ImageValidator.SUPPORTED_FORMATS:
            return False

        # Check file size
        if path.stat().st_size > ImageValidator.MAX_FILE_SIZE:
            return False

        return True

    @staticmethod
    def validate_image_quality(image_path: str) -> Dict[str, Any]:
        """
        Validate image quality for analysis.

        Args:
            image_path: Path to image file

        Returns:
            Quality assessment dict
        """
        # TODO: Implement image quality validation
        pass


class AnalysisValidator:
    """Validator for analysis requests and data."""

    VALID_ANALYSIS_TYPES = [
        "damage_detection",
        "condition_assessment",
        "market_analysis",
        "pricing",
    ]

    @staticmethod
    def validate_analysis_types(analysis_types: List[str]) -> bool:
        """Validate analysis types."""
        return all(
            analysis_type in AnalysisValidator.VALID_ANALYSIS_TYPES
            for analysis_type in analysis_types
        )

    @staticmethod
    def validate_vehicle_data(vehicle_data: Dict) -> bool:
        """Validate vehicle data for analysis."""
        required_fields = ["vehicle_id", "make", "model", "year"]
        return all(field in vehicle_data for field in required_fields)

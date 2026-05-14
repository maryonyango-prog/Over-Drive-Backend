"""Calculation utilities for analysis."""

from typing import Dict, List, Optional


class DamageCalculator:
    """Calculator for damage-related values."""

    @staticmethod
    def calculate_total_repair_cost(damages: List[Dict]) -> Dict[str, float]:
        """
        Calculate total repair cost from damages.

        Args:
            damages: List of damage items

        Returns:
            Dict with min and max repair costs
        """
        total_min = sum(d.get("estimated_cost_min", 0) for d in damages)
        total_max = sum(d.get("estimated_cost_max", 0) for d in damages)

        return {"min": total_min, "max": total_max, "avg": (total_min + total_max) / 2}

    @staticmethod
    def calculate_severity_percentage(damages: List[Dict]) -> Dict[str, float]:
        """
        Calculate percentage of damages by severity.

        Args:
            damages: List of damage items

        Returns:
            Dict with severity percentages
        """
        total = len(damages)
        if total == 0:
            return {"minor": 0, "moderate": 0, "severe": 0}

        minor_count = sum(1 for d in damages if d.get("severity") == "minor")
        moderate_count = sum(1 for d in damages if d.get("severity") == "moderate")
        severe_count = sum(1 for d in damages if d.get("severity") == "severe")

        return {
            "minor": (minor_count / total) * 100,
            "moderate": (moderate_count / total) * 100,
            "severe": (severe_count / total) * 100,
        }


class ConditionCalculator:
    """Calculator for condition-related values."""

    @staticmethod
    def calculate_overall_score(scores: Dict[str, float]) -> float:
        """
        Calculate overall condition score from individual scores.

        Args:
            scores: Dict with individual component scores

        Returns:
            Overall score (0-100)
        """
        if not scores:
            return 0

        return sum(scores.values()) / len(scores)

    @staticmethod
    def grade_from_score(score: float) -> str:
        """
        Convert score to grade.

        Args:
            score: Score value (0-100)

        Returns:
            Grade (excellent, good, fair, poor)
        """
        if score >= 85:
            return "excellent"
        elif score >= 70:
            return "good"
        elif score >= 50:
            return "fair"
        else:
            return "poor"


class PricingCalculator:
    """Calculator for pricing-related values."""

    @staticmethod
    def calculate_depreciation(
        base_price: float, vehicle_year: int, current_year: int = 2024
    ) -> float:
        """
        Calculate depreciation adjustment.

        Args:
            base_price: Base vehicle price
            vehicle_year: Year of manufacture
            current_year: Current year

        Returns:
            Depreciation percentage
        """
        age = current_year - vehicle_year
        # Simplified depreciation: 15% first year, 10% per year after
        if age == 0:
            return 0
        elif age == 1:
            return base_price * 0.15
        else:
            return base_price * (0.15 + (age - 1) * 0.10)

    @staticmethod
    def apply_condition_adjustment(
        base_price: float, condition_score: float
    ) -> float:
        """
        Apply condition-based adjustment to price.

        Args:
            base_price: Base price
            condition_score: Condition score (0-100)

        Returns:
            Adjusted price
        """
        adjustment_factor = (condition_score - 50) / 100  # -0.5 to 0.5
        return base_price * (1 + adjustment_factor)

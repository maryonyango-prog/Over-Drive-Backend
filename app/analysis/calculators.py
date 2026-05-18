"""Calculations for damage, condition and pricing."""

from typing import Dict, List


class DamageCalculator:
    """Works out repair costs and damage severity."""

    @staticmethod
    def calculate_total_repair_cost(damages: List[Dict]) -> Dict[str, float]:
        """Add up all repair costs from the list of damages."""
        total_min = sum(d.get("estimated_cost_min", 0) for d in damages)
        total_max = sum(d.get("estimated_cost_max", 0) for d in damages)
        return {
            "min": total_min,
            "max": total_max,
            "avg": (total_min + total_max) / 2
        }

    @staticmethod
    def calculate_severity_percentage(damages: List[Dict]) -> Dict[str, float]:
        """Work out what percentage of damages are minor, moderate or severe."""
        total = len(damages)
        if total == 0:
            return {"minor": 0, "moderate": 0, "severe": 0}

        return {
            "minor":    (sum(1 for d in damages if d.get("severity") == "minor")    / total) * 100,
            "moderate": (sum(1 for d in damages if d.get("severity") == "moderate") / total) * 100,
            "severe":   (sum(1 for d in damages if d.get("severity") == "severe")   / total) * 100,
        }


class ConditionCalculator:
    """Works out the overall condition score and grade of the car."""

    @staticmethod
    def calculate_overall_score(scores: Dict[str, float]) -> float:
        """Average all the individual scores to get one overall score."""
        if not scores:
            return 0
        return sum(scores.values()) / len(scores)

    @staticmethod
    def grade_from_score(score: float) -> str:
        """Turn a number score into a simple grade — excellent, good, fair or poor."""
        if score >= 85:
            return "excellent"
        elif score >= 70:
            return "good"
        elif score >= 50:
            return "fair"
        else:
            return "poor"


class PricingCalculator:
    """Works out the car price based on age and condition."""

    @staticmethod
    def calculate_depreciation(base_price: float, vehicle_year: int, current_year: int = 2024) -> float:
        """
        Reduce the price based on how old the car is.
        Loses 15% in the first year, then 10% every year after.
        """
        age = current_year - vehicle_year
        if age == 0:
            return 0
        elif age == 1:
            return base_price * 0.15
        else:
            return base_price * (0.15 + (age - 1) * 0.10)

    @staticmethod
    def apply_condition_adjustment(base_price: float, condition_score: float) -> float:
        """
        Adjust the price up or down based on condition.
        Good condition = higher price. Bad condition = lower price.
        """
        adjustment_factor = (condition_score - 50) / 100
        return base_price * (1 + adjustment_factor)
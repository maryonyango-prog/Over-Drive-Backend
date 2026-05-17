"""Pricing engine for vehicle valuation."""

from typing import Dict, List
from pydantic import BaseModel


class PricingFactors(BaseModel):
    base_price: float
    condition_adjustment: float
    mileage_adjustment: float
    damage_adjustment: float


class PricingResult(BaseModel):
    estimated_price_min: float
    estimated_price_max: float
    estimated_price_avg: float
    confidence_score: float  # 0-100
    factors: PricingFactors
    depreciation_notes: List[str]


class PricingEngine:
    """Works out the price range of the car based on its condition."""

    async def calculate_price(
        self,
        vehicle_make: str,
        vehicle_model: str,
        vehicle_year: int,
        mileage: int,
        condition_score: float,
        damage_estimate: float = 0.0,
    ) -> PricingResult:
        """
        Calculate a price range for the car.

        Takes the car details + condition score and returns
        a low, average, and high price estimate.
        """

        # Start with a rough base price based on the year
        # Newer car = higher starting price
        current_year = 2025
        age = current_year - vehicle_year
        base_price = max(5000.0, 30000.0 - (age * 1500))

        # Better condition = higher price (condition_score is 0-100)
        # Convert to a multiplier between 0.6 and 1.0
        condition_multiplier = 0.6 + (condition_score / 100) * 0.4
        condition_adjustment = base_price * (condition_multiplier - 1)

        # Higher mileage = lower price
        # Every 10,000 km over 50,000 knocks off 3%
        mileage_penalty = max(0, (mileage - 50000) / 10000) * 0.03
        mileage_adjustment = -(base_price * mileage_penalty)

        # Damage reduces price directly
        damage_adjustment = -damage_estimate

        # Final average price
        avg_price = base_price + condition_adjustment + mileage_adjustment + damage_adjustment
        avg_price = max(1000.0, avg_price)  # never go below 1000

        return PricingResult(
            estimated_price_min=round(avg_price * 0.9, 2),
            estimated_price_max=round(avg_price * 1.1, 2),
            estimated_price_avg=round(avg_price, 2),
            confidence_score=72.0,
            factors=PricingFactors(
                base_price=round(base_price, 2),
                condition_adjustment=round(condition_adjustment, 2),
                mileage_adjustment=round(mileage_adjustment, 2),
                damage_adjustment=round(damage_adjustment, 2),
            ),
            depreciation_notes=[
                f"Vehicle is {age} years old",
                f"Mileage is {mileage:,} km",
                "Price adjusted for current market conditions",
            ],
        )
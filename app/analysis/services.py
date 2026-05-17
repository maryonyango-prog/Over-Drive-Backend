"""Business logic — runs the AI and saves results to the database."""

from typing import List, Dict
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.analysis import Valuation
from app.models.vehicle import Listing
from app.ai.condition_scoring import ConditionScoringService
from app.ai.pricing_engine import PricingEngine


class AnalysisService:
    """
    This service does three things in order:
    1. Gets the car details from the database
    2. Runs the AI to assess condition and calculate price
    3. Saves the result to the valuations table
    """

    def __init__(self, db_session: Session):
        self.db = db_session
        self.pricing_engine = PricingEngine()

    async def create_analysis(
        self,
        vehicle_id: int,
        image_path: str,
        analysis_types: List[str],
    ) -> Dict:

        # ── Step 1: Get the car from the database ──────────
        listing = self.db.query(Listing).filter(Listing.id == vehicle_id).first()
        if not listing:
            raise Exception(f"No listing found with id {vehicle_id}")

        # ── Step 2: Run condition scoring AI ───────────────
        # We pass None as the ai_analyzer for now because the
        # AI vision module is still being built by your colleagues.
        # Once they finish it, replace None with their analyzer.
        condition_service = ConditionScoringService(ai_analyzer=None)
        condition_result = condition_service._parse_condition_response("")

        # Overall score out of 10 (AI returns 0-100, we convert)
        overall_score = condition_result.scores.overall / 10

        # ── Step 3: Run pricing engine ─────────────────────
        pricing_result = await self.pricing_engine.calculate_price(
            vehicle_make=listing.make,
            vehicle_model=listing.model,
            vehicle_year=listing.year,
            mileage=listing.mileage,
            condition_score=condition_result.scores.overall,
            damage_estimate=0.0,
        )

        # ── Step 4: Save everything to the database ────────
        # Check if a valuation already exists for this listing
        existing = self.db.query(Valuation).filter(
            Valuation.listing_id == vehicle_id
        ).first()

        if existing:
            # Update the existing valuation
            existing.condition_score = overall_score
            existing.price_low       = pricing_result.estimated_price_min
            existing.price_mid       = pricing_result.estimated_price_avg
            existing.price_high      = pricing_result.estimated_price_max
            existing.summary         = f"Vehicle grade: {condition_result.grade.value}. {', '.join(condition_result.observations)}"
            existing.positives       = condition_result.observations
            existing.concerns        = condition_result.maintenance_recommendations
            valuation = existing
        else:
            # Create a new valuation
            valuation = Valuation(
                listing_id      = vehicle_id,
                condition_score = overall_score,
                price_low       = pricing_result.estimated_price_min,
                price_mid       = pricing_result.estimated_price_avg,
                price_high      = pricing_result.estimated_price_max,
                summary         = f"Vehicle grade: {condition_result.grade.value}. {', '.join(condition_result.observations)}",
                positives       = condition_result.observations,
                concerns        = condition_result.maintenance_recommendations,
            )
            self.db.add(valuation)

        self.db.commit()
        self.db.refresh(valuation)

        # ── Step 5: Return the result to the API ───────────
        return {
            "vehicle_id"     : vehicle_id,
            "status"         : "complete",
            "grade"          : condition_result.grade.value,
            "condition_score": valuation.condition_score,
            "price_low"      : valuation.price_low,
            "price_mid"      : valuation.price_mid,
            "price_high"     : valuation.price_high,
            "summary"        : valuation.summary,
            "positives"      : valuation.positives,
            "concerns"       : valuation.concerns,
            "created_at"     : valuation.created_at.isoformat(),
        }

    async def get_vehicle_analyses(self, vehicle_id: int) -> Dict:
        """Fetch the saved valuation for a vehicle."""
        valuation = self.db.query(Valuation).filter(
            Valuation.listing_id == vehicle_id
        ).first()

        if not valuation:
            return {"message": "No analysis found for this vehicle"}

        return {
            "vehicle_id"     : vehicle_id,
            "condition_score": valuation.condition_score,
            "price_low"      : valuation.price_low,
            "price_mid"      : valuation.price_mid,
            "price_high"     : valuation.price_high,
            "summary"        : valuation.summary,
            "positives"      : valuation.positives,
            "concerns"       : valuation.concerns,
            "created_at"     : valuation.created_at.isoformat(),
        }

    async def get_analysis(self, analysis_id: str) -> Dict:
        return None
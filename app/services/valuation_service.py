# app/services/valuation_service.py
from statistics import median
import traceback
from app.database.database import db

# Safe import for MarketListing
try:
    from app.models.market_listing import MarketListing
    MARKET_LISTING_AVAILABLE = True
except ImportError:
    MarketListing = None
    MARKET_LISTING_AVAILABLE = False
    print("  MarketListing model not found. Using fallback valuation logic.")


class ValuationService:
    EXPECTED_ANNUAL_MILEAGE = 15000

    @staticmethod
    def get_comparables(vehicle):
        if not MARKET_LISTING_AVAILABLE:
            print("  MarketListing table not available. Returning empty comparables.")
            return []

        try:
            make = (getattr(vehicle, 'make', '') or "").strip().lower()
            model = (getattr(vehicle, 'model', '') or "").strip().lower()
            year = getattr(vehicle, 'year', 2024)

            print(" Searching comparables:")
            print(f" MAKE: {make}")
            print(f" MODEL: {model}")
            print(f" YEAR: {year}")

            query = MarketListing.query.filter(
                MarketListing.make.ilike(f"%{make}%")
            )

            if "corolla" in model or "axio" in model:
                query = query.filter(
                    db.or_(
                        MarketListing.model.ilike("%corolla%"),
                        MarketListing.model.ilike("%axio%"),
                        MarketListing.title.ilike("%corolla%") if hasattr(MarketListing, 'title') else False,
                        MarketListing.title.ilike("%axio%") if hasattr(MarketListing, 'title') else False
                    )
                )

            # Prioritize newer cars
            comparables = query.filter(
                MarketListing.year.between(year - 12, year + 1)
            ).order_by(MarketListing.year.desc(), MarketListing.price.desc()).limit(150).all()

            print(f" FOUND: {len(comparables)} comparables")

            if len(comparables) < 15:
                print(" Widening search...")
                comparables = query.filter(
                    MarketListing.year.between(year - 18, year + 3)
                ).limit(100).all()

            return comparables

        except Exception as e:
            print(f" Error in get_comparables: {e}")
            traceback.print_exc()
            return []

    @staticmethod
    def calculate_market_average(comparables):
        if not comparables:
            return 0
        prices = [float(c.price) for c in comparables if c.price and float(c.price) > 300000]
        return int(median(prices)) if prices else 0

    @staticmethod
    def calculate_mileage_adjustment(vehicle):
        try:
            current_year = 2026
            year = getattr(vehicle, 'year', 2024)
            mileage = getattr(vehicle, 'mileage', 0)
            expected = (current_year - year) * ValuationService.EXPECTED_ANNUAL_MILEAGE
            return int((mileage - expected) * -3)
        except:
            return 0

    @staticmethod
    def condition_multiplier(score):
        if score >= 90: return 1.08
        elif score >= 80: return 1.04
        elif score >= 70: return 1.00
        elif score >= 60: return 0.93
        return 0.85

    @staticmethod
    def calculate(vehicle, condition_score=75):
        try:
            comparables = ValuationService.get_comparables(vehicle)
            market_average = ValuationService.calculate_market_average(comparables)

            # Fallback for new cars or no data
            if market_average < 900000:
                market_average = getattr(vehicle, 'asking_price', 2400000) or 2400000

            mileage_adjustment = ValuationService.calculate_mileage_adjustment(vehicle)
            base_price = market_average + mileage_adjustment
            multiplier = ValuationService.condition_multiplier(condition_score)
            final_estimate = max(950000, int(base_price * multiplier))

            return {
                "market_average": market_average,
                "mileage_adjustment": mileage_adjustment,
                "condition_score": condition_score,
                "final_estimate": final_estimate,
                "confidence_score": min(50 + len(comparables) * 2, 95),
                "comparable_vehicles": len(comparables),
                "comparables": [
                    {
                        "make": getattr(c, 'make', ''),
                        "model": getattr(c, 'model', ''),
                        "year": getattr(c, 'year', None),
                        "price": c.price,
                        "mileage": getattr(c, 'mileage', None),
                        "location": getattr(c, 'location', '')
                    } for c in comparables[:6]
                ]
            }

        except Exception as e:
            print(f"CRITICAL ERROR in valuation: {e}")
            traceback.print_exc()
            fallback = getattr(vehicle, 'asking_price', 2400000) or 2400000
            return {
                "market_average": fallback,
                "final_estimate": fallback,
                "confidence_score": 60,
                "comparable_vehicles": 0,
                "error": str(e)
            }
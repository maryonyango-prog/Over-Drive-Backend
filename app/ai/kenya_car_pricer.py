# app/ai/kenya_car_pricer.py
import pandas as pd
from pathlib import Path

class KenyaCarPricer:
    def __init__(self):
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load Kenyan car market data from Jiji"""
        try:
            file_path = Path(__file__).parent.parent / "data" / "JijiCarsRawDataFinal.xlsx"
            
            if not file_path.exists():
                print(f"⚠️ File not found: {file_path}")
                return
                
            self.df = pd.read_excel(file_path)
            print(f"✅ Successfully loaded {len(self.df):,} real Kenyan car records from Jiji")

            # Clean price and year columns
            self.df['Price_clean'] = self.df['Price'].astype(str).str.replace(r'[^\d]', '', regex=True)
            self.df['Price_clean'] = pd.to_numeric(self.df['Price_clean'], errors='coerce')
            self.df['YOM'] = pd.to_numeric(self.df['YOM'], errors='coerce')
            
        except Exception as e:
            print(f"❌ Failed to load car data: {e}")
            self.df = None

    def get_market_price(self, make, model, year, mileage=0):
        """Get realistic market price based on real Jiji data"""
        if self.df is None or not year:
            return {"low": 1500000, "mid": 2200000, "high": 2800000, "recommended": 2200000, "sample_size": 0}

        year = int(year)
        mileage = int(mileage) if mileage else 0

        # Find similar vehicles
        mask = (
            self.df['Make'].str.contains(make, case=False, na=False) &
            self.df['Model'].str.contains(model, case=False, na=False) &
            (self.df['YOM'] == year)
        )
        similar = self.df[mask]

        # Broaden search if needed
        if len(similar) < 5:
            mask = self.df['Make'].str.contains(make, case=False, na=False)
            similar = self.df[mask]

        if len(similar) == 0:
            return {"low": 1400000, "mid": 2000000, "high": 2600000, "recommended": 2000000, "sample_size": 0}

        prices = similar['Price_clean'].dropna()
        if len(prices) == 0:
            return {"low": 1400000, "mid": 2000000, "high": 2600000, "recommended": 2000000, "sample_size": len(similar)}

        low = int(prices.quantile(0.15))
        mid = int(prices.median())
        high = int(prices.quantile(0.85))
        recommended = mid

        # Adjust for high mileage
        if mileage > 120000:
            recommended = int(recommended * 0.82)

        return {
            "low": max(700000, low),
            "mid": recommended,
            "high": high,
            "recommended": recommended,
            "sample_size": len(similar)
        }


# Global instance
kenya_pricer = KenyaCarPricer()
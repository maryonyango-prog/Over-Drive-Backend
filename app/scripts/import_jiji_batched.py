import sys
import os
sys.path.insert(0, os.path.abspath('.'))

import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
from app.config import Config

print(" Starting batched import (safer for Supabase)...")

df = pd.read_csv("cleaned_jiji_listings.csv")
print(f"Loaded {len(df)} records")

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, echo=False)

with engine.connect() as conn:
    print("Clearing old data...")
    conn.execute(text("TRUNCATE TABLE market_listings RESTART IDENTITY;"))
    conn.commit()

    print("Starting batched insert...")
    batch_size = 1500
    total = 0

    for i in range(0, len(df), batch_size):
        batch = []
        batch_df = df.iloc[i:i+batch_size]
        
        for _, row in batch_df.iterrows():
            try:
                batch.append({
                    "source": "Jiji",
                    "title": f"{row.get('make','')} {row.get('model','')}",
                    "make": row.get('make'),
                    "model": row.get('model'),
                    "year": int(row['year']) if pd.notna(row.get('year')) else None,
                    "mileage": int(row['mileage']) if pd.notna(row.get('mileage')) else None,
                    "price": float(row['price']),
                    "location": row.get('location', 'Nairobi'),
                    "scraped_at": datetime.utcnow()
                })
            except:
                continue

        if batch:
            conn.execute(text("""
                INSERT INTO market_listings (source, title, make, model, year, mileage, price, location, scraped_at)
                VALUES (:source, :title, :make, :model, :year, :mileage, :price, :location, :scraped_at)
            """), batch)
            conn.commit()
            total += len(batch)
            print(f"   Batch inserted - Total so far: {total}")

print(f"\n IMPORT FINISHED! Total records: {total}")

# Final stats
with engine.connect() as conn:
    total_count = conn.execute(text("SELECT COUNT(*) FROM market_listings")).scalar()
    toyota = conn.execute(text("SELECT COUNT(*) FROM market_listings WHERE make ILIKE '%toyota%'")).scalar()
    corolla = conn.execute(text("SELECT COUNT(*) FROM market_listings WHERE model ILIKE '%corolla%'")).scalar()
    
    print(f"\n Stats:")
    print(f"Total: {total_count}")
    print(f"Toyota: {toyota}")
    print(f"Corolla: {corolla}")

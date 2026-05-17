from sqlalchemy import text
from app.database.database import engine

def test_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Database connection successful.")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
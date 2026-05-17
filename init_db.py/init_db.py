import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.database.database import Base, engine
import app.models  # noqa

def init_db():
    print("⚠️  Dropping all existing tables...")
    Base.metadata.drop_all(bind=engine)

    print("🔨 Creating all Over Drive tables...")
    Base.metadata.create_all(bind=engine)

    print("\n✅ Done! Tables created:")
    from sqlalchemy import inspect
    for table in inspect(engine).get_table_names():
        print(f"   ✓ {table}")

if __name__ == "__main__":
    init_db()
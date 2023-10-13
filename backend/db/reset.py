from sqlalchemy import text

from db import engine
from db.models import Base

def reset_database():
    Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    reset_database()
    print("Database reset!")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print(result.fetchone())
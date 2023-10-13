from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

logging.basicConfig()

# Enable sqlalchemy logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

# Set Database constants
DATABASE_URL = "postgresql://test:test@localhost:5432/test-db"

engine = create_engine(DATABASE_URL, echo=True)
# Create Session Factory
SessionLocal = sessionmaker(bind=engine)
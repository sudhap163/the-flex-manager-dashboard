
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.review_orm import Base
from app.utils.log import logger
import os

# Create a SQLAlchemy engine
engine = create_engine(os.getenv("DATABASE_URL"))

# Create a session local class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_connection():
    """Provides a new SQLAlchemy database session. This is a dependency for FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initializes the database and creates the 'reviews' table if it doesn't exist."""
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialization complete.")

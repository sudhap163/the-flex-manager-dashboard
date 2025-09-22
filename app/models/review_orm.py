""" SQLAlchemy ORM Model """

from sqlalchemy import Column, String, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ReviewORM(Base):
    """SQLAlchemy ORM model for the 'reviews' table."""
    __tablename__ = 'reviews'
    id = Column(String, primary_key=True)
    public_review = Column(String)
    reviewer_name = Column(String)
    submitted_at = Column(String)
    category_ratings = Column(JSON)
    listing_name = Column(String)
    channel = Column(String)
    type = Column(String)
    is_approved = Column(Integer)

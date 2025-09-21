""" SQLAlchemy ORM Model """

from sqlalchemy import Column, String, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ReviewORM(Base):
    """SQLAlchemy ORM model for the 'reviews' table."""
    __tablename__ = 'reviews'
    id = Column(String, primary_key=True)
    publicReview = Column(String)
    reviewerName = Column(String)
    submittedAt = Column(String)
    categoryRatings = Column(JSON)
    listingName = Column(String)
    channel = Column(String)
    type = Column(String)
    isApproved = Column(Integer)

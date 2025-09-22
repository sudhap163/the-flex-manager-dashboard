from pydantic import BaseModel
from typing import List

class CategoryRating(BaseModel):
    category: str
    rating: int

class Review(BaseModel):
    id: str
    public_review: str
    reviewer_name: str
    listing_name: str
    channel: str
    submitted_at: str
    type: str
    category_ratings: List[CategoryRating]
    is_approved: int

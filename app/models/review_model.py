from pydantic import BaseModel
from typing import List

class CategoryRating(BaseModel):
    category: str
    rating: int

class Review(BaseModel):
    id: str
    publicReview: str
    reviewerName: str
    listingName: str
    channel: str
    submittedAt: str
    type: str
    categoryRatings: List[CategoryRating]
    isApproved: int

# class UpdateReviewStatus(BaseModel):
#     reviewId: str = Field(alias='reviewId')
#     isApproved: bool = Field(alias='isApproved')

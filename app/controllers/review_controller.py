from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from sqlalchemy.orm import Session

from core.database import get_db_connection
from models.review_model import Review
from services import review_service


router = APIRouter()

@router.get("/reviews", response_model=Dict[str, Any])
def get_all_reviews(session: Session = Depends(get_db_connection)):
    """Returns a list of all reviews."""
    all_reviews = review_service.get_all_approved_reviews(session)
    return {"status": "success", "result": all_reviews}

@router.get("/reviews/hostaway", response_model=Dict[str, Any])
def get_hostaway_reviews():
    """Returns list of reviews from Hostaway"""
    hostaway_reviews = review_service.get_hostaway_reviews()
    return {"status": "success", "result": hostaway_reviews}

@router.get("/reviews/approved/{listing_name}", response_model=Dict[str, Any])
def get_approved_reviews(listing_name: str, session: Session = Depends(get_db_connection)):
    """Returns a list of approved reviews for a specific listing."""
    approved_reviews = review_service.get_approved_reviews_by_listing(listing_name, session)
    return {"status": "success", "result": approved_reviews}

@router.post("/reviews/save", response_model=Dict[str, Any])
def save_approved_reviews(review: Review, session: Session = Depends(get_db_connection)):
    """Saves approved reviews to the database."""
    saved_count = review_service.save_approved_review_to_db(review, session)
    if saved_count > 0:
        return {"success": True, "message": f"{saved_count} reviews saved successfully."}
    else:
        raise HTTPException(status_code=500, detail="Failed to save reviews.")

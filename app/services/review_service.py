import json
import requests

from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Any

from models.review_model import Review
from models.review_orm import ReviewORM
from utils.log import logger
from utils.config import configuration
from utils.dummy_hostaway_review_data import DUMMY_HOSTAWAY_REVIEW_DATA

def get_all_approved_reviews(session: Session) -> List[Dict[str, Any]]:
    """Fetches all approved reviews from the database using SQLAlchemy."""
    logger.debug("Fetching all approved reviews")
    try:
        reviews = session.query(ReviewORM).all()
        
        reviews_list = []
        for review in reviews:
            review_dict = review.__dict__
            review_dict.pop('_sa_instance_state', None)
            reviews_list.append(review_dict)

        logger.info(f"Found {len(reviews_list)} approved reviews.")
        return reviews_list
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching approved reviews: {e}")
        return []

def get_hostaway_reviews() -> List[Dict[str, Any]]:
    """Fetches reviews from Hostaway."""

    # 1. Get access token
    token_headers = {
        "Cache-control": "no-cache",
        "Content-type": "application/x-www-form-urlencoded"
    }
    token_data = {
        "grant_type": "client_credentials",
        "client_id": configuration["hostaway_account_id"],
        "client_secret": configuration["hostaway_api_key"],
        "scope": "general"
    }
    
    try:
        token_response = requests.post(configuration["hostaway_auth_endpoint"], headers=token_headers, data=token_data, timeout=5)
        token_response.raise_for_status()
        token_type = token_response.json().get("token_type")
        access_token = token_response.json().get("access_token")
    except requests.exceptions.RequestException as e:
        print(f"Error getting Hostaway access token: {e}")
        return [] # Return empty list if token cannot be obtained
    
    logger.debug(f"Hostaway access token: {access_token}")

    if not access_token:
        print("Failed to retrieve Hostaway access token.")
        return []

    # 2. Use access token to get reviews
    reviews_headers = {
        "Cache-control": "no-cache",
        "Authorization": f"{token_type} {access_token}"
    }

    try:
        reviews_response = requests.get(configuration["hostaway_review_endpoint"], headers=reviews_headers, timeout=5)
        reviews_response.raise_for_status()
        hostaway_review_data = reviews_response.json().get("result")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Hostaway reviews: {e}")
        return []
    
    logger.debug(f"Hostaway reviews: {hostaway_review_data}")
    
    if not hostaway_review_data:
        mock_data = get_mocked_hostaway_data()
        logger.debug(f"Mocked Hostaway reviews: {mock_data}")
        hostaway_review_data = parse_hostaway_review_data(mock_data)

    return hostaway_review_data
    
def get_mocked_hostaway_data() -> List[Dict[str, Any]]:
    return DUMMY_HOSTAWAY_REVIEW_DATA.get("result")

def parse_hostaway_review_data(reviews_list: List[Dict[str, Any]]) -> List[Review]:
    reviews = []
    
    for review_data in reviews_list:
        logger.debug(f"Review data: {review_data}")
        try:
            # Manually map fields to match the Pydantic model
            mapped_data = {
                "id": review_data.get("id"),
                "publicReview": review_data.get("publicReview"),
                "reviewerName": review_data.get("guestName"),
                "submittedAt": review_data.get("submittedAt"),
                "categoryRatings": review_data.get("reviewCategory"),
                "listingName": review_data.get("listingName"),
                "type": review_data.get("type"),
                "isApproved": 0,
                "channel": "Hostaway"
            }

            logger.debug(f"Mapped review data: {mapped_data}")
            
            review_item = Review.model_validate(mapped_data)
            reviews.append(review_item)
        except ValidationError as e:
            print(f"Error validating review data: {e}")
            continue
    
    return reviews

def get_approved_reviews_by_listing(listing_name: str, session: Session) -> List[Dict[str, Any]]:
    """Fetches approved reviews for a specific listing from the database using SQLAlchemy."""
    logger.debug(f"Fetching approved reviews for listing: {listing_name}")
    try:
        reviews = session.query(ReviewORM).filter(
            ReviewORM.isApproved == 1,
            ReviewORM.listingName == listing_name
        ).all()
        
        reviews_list = []
        for review in reviews:
            review_dict = review.__dict__
            review_dict.pop('_sa_instance_state', None)
            reviews_list.append(review_dict)

        logger.info(f"Found {len(reviews_list)} approved reviews for '{listing_name}'.")
        return reviews_list
    except SQLAlchemyError as e:
        logger.error(f"Database error fetching approved reviews: {e}")
        return []

def save_approved_review_to_db(review: Review, session: Session) -> int:
    """
    Saves a single approved review to the database using SQLAlchemy.
    """
    logger.debug(f"Attempting to save approved review: {review}")
    try:
        review_orm = ReviewORM(
            id=review.id,
            publicReview=review.publicReview,
            reviewerName=review.reviewerName,
            submittedAt=review.submittedAt,
            categoryRatings=json.dumps([r.model_dump() for r in review.categoryRatings]),
            listingName=review.listingName,
            channel=review.channel,
            type=review.type,
            isApproved=1
        )

        logger.debug(f"Review ORM: {review_orm}")
        
        session.merge(review_orm)
        session.commit()
        
        logger.info(f"Successfully saved approved review ID: {review.id}.")
        return 1

    except SQLAlchemyError as e:
        # Rollback the session on a database error
        logger.error(f"Database error saving approved review: {e}")
        session.rollback()
        return 0

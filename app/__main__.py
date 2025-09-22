from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from controllers import review_controller, html_controller
from core.database import init_db
from utils.log import logger

import uvicorn

# Create FastAPI app
fastAPI_app = FastAPI()

# Enable CORS for all origins
fastAPI_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (CSS, JS, images)
fastAPI_app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
fastAPI_app.include_router(review_controller.router, prefix="/api")      # API routes
fastAPI_app.include_router(html_controller.router)                       # HTML view routes

# Initialize database
init_db()

# App runner
if __name__ == "__main__":
    logger.info("Application started..")
    uvicorn.run(fastAPI_app, host="0.0.0.0", port=80)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.controllers import review_controller, html_controller
from app.core.database import init_db
from app.utils.log import logger

import uvicorn

# Create FastAPI app
app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (CSS, JS, images)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(review_controller.router, prefix="/api")      # API routes
app.include_router(html_controller.router)                       # HTML view routes

# Initialize database, does not work on Serverless
init_db()

# App runner
if __name__ == "__main__":
    logger.info("Application started..")
    uvicorn.run(app, host="0.0.0.0", port=80)

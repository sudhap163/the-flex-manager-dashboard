from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.database import init_db

# Router for HTML views
router = APIRouter()

# Load templates from app/templates
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    init_db()
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/property_details/189 Hoxton Street", response_class=HTMLResponse)
async def serve_property_details(request: Request):
    return templates.TemplateResponse("property_details.html", {"request": request})

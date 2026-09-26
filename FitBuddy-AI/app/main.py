from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .config import get_settings
from .database import init_db
from .routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


settings = get_settings()

app = FastAPI(
    title="FitBuddy – AI Fitness Plan Generator",
    description=(
        "AI-powered 7-day workout planning with feedback-based updates."
    ),
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan,
)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"request": request, "app_name": settings.app_name},
    )
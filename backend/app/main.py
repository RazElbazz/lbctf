from fastapi import FastAPI
from fastapi.routing import APIRoute

from app.core.config import settings
from app.api.main import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
)

app.include_router(api_router, prefix=settings.API_V1_STR)

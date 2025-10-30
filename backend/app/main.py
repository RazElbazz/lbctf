from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.core.db import init_db, engine
from app.api.main import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ---- Startup ----
    init_db()  # create tables, etc.
    yield
    # ---- Shutdown ----
    # For a sync SQLAlchemy engine, dispose() is synchronous.
    # It's safe to call here without 'await'.
    engine.dispose()

app = FastAPI(lifespan=lifespan, 
    title=settings.PROJECT_NAME,)

app.include_router(api_router, prefix=settings.API_V1_STR)

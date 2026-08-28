from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.models import System, User  # noqa: F401 — ensures models register on Base.metadata
from app.routers import auth, systems


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Dev-friendly auto-create. Once the schema stabilizes, switch to Alembic
    # migrations (`alembic upgrade head`) instead of create_all.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(systems.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

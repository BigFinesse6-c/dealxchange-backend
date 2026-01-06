# app/main.py
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.db.seed import seed_admin
from sqlalchemy import select
from app.models.user import User
from app.core.config import settings
from app.db.database import init_models, AsyncSession
from app.api.v1.api import api_router  # This will include auth & listings routes
from app.api.v1.storage import  router as storage_router
from app.api.v1.auth import router as auth_router
from app.api.v1.listings import router 

# Initialize FastAPI app
app = FastAPI(
    title=getattr(settings, "PROJECT_NAME", "CrownKey AI API"),
    description="Backend API for CrownKey AI platform",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

origins = settings.CORS_ORIGINS.split(",")


# Enable CORS (allow frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Replace '*' with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# Startup event: init DB
# ------------------------
@app.on_event("startup")
async def on_startup():
    """
    Runs at app startup to create tables if they don't exist.
    """
    await init_models()
    print("✅ Database tables initialized")

# ------------------------
# Register API routers
# ------------------------
app.include_router(api_router, prefix="/api/v1")
app.include_router(router)
app.include_router(storage_router)


# ------------------------
# Root endpoint
# ------------------------
@app.get("/", tags=["Root"])
async def root():
    return {"message": f"{getattr(settings, 'PROJECT_NAME', 'DealXchange')} API is ready"}
    
@app.get("/health")
def health():
    return {"status": "ok"}

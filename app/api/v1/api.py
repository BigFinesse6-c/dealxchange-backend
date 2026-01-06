from fastapi import APIRouter
from app.api.v1 import auth, listings, deals

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(listings.router, prefix="", tags=["listings"])
api_router.include_router(deals.router, prefix="/api/v1")

#"http://localhost:8000/api/v1/buyer-feed"

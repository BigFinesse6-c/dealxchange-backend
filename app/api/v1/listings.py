# app/api/v1/listings.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
import shutil
import os
from pydantic import BaseModel
from app.api.v1.ws import broadcast_new_listing
from app.db.database import get_db
from app.models.listing import Listing
from app.models.user import User, UserRole
from app.schemas.listing import ListingRead
from app.core.auth import get_current_user
from fastapi import WebSocket
from app.core.ws_manager import manager

router = APIRouter(prefix="/listings", tags=["Listings"])
bearer_scheme = HTTPBearer()
STATIC_IMAGE_PATH = "app/static/images"
os.makedirs(STATIC_IMAGE_PATH, exist_ok=True)

BACKEND_URL = "http://127.0.0.1:800"

async def get_current_user(
    token: HTTPAuthorizationCredentials = Security(bearer_scheme),
):
    user_id = verify_access_token(token.credentials)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id


router = APIRouter()
STATIC_IMAGE_PATH = "app/static/images"
os.makedirs(STATIC_IMAGE_PATH, exist_ok=True)

BACKEND_URL = "http://127.0.0.1:800"


# -------------------------
# APPROVE LISTING BODY MODEL
# -------------------------
class ApproveListing(BaseModel):
    approved: bool


# -------------------------
# CREATE LISTING
# -------------------------
@router.post("/listings", response_model=ListingRead)
async def create_listing(
    title: str = Form(...),
    address: str = Form(...),
    zip_code: str = Form(...),
    year_built: Optional[int] = Form(None),
    square_footage: int = Form(...),
    price: int = Form(...),
    description: Optional[str] = Form(None),
    approved: bool = Form(False),
    image: Optional[UploadFile] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Save image
    image_url = None
    if image:
        file_path = os.path.join(STATIC_IMAGE_PATH, image.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(image.file, f)
        image_url = f"{BACKEND_URL}/static/images/{image.filename}"

    listing = Listing(
        title=title,
        address=address,
        zip_code=zip_code,
        year_built=year_built,
        square_footage=square_footage,
        price=price,
        description=description,
        approved=approved,
        image_url=image_url,
        owner_id=current_user.id,
    )
    db.add(listing)
    await db.commit()
    await db.refresh(listing)

    return ListingRead.from_orm(listing)


# -------------------------
# GET ALL LISTINGS (public)
# -------------------------
@router.get("/listings", response_model=List[ListingRead])
async def get_listings(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Listing).where(Listing.approved == True)
    )
    return result.scalars().all()

# -------------------------
# ADMIN: APPROVE LISTING
# -------------------------
@router.patch("/admin/listings/{listing_id}", response_model=ListingRead)
async def approve_listing(
    listing_id: int,
    body: ApproveListing,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")

    result = await db.execute(select(Listing).where(Listing.id == listing_id))
    listing = result.scalar_one_or_none()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    listing.approved = body.approved
    await db.commit()
    await db.refresh(listing)

    # ✅ Broadcast to all connected buyers
    if listing.approved:
        await manager.broadcast({
            "id": listing.id,
            "title": listing.title,
            "address": listing.address,
            "zip_code": listing.zip_code,
            "year_built": listing.year_built,
            "square_footage": listing.square_footage,
            "price": listing.price,
            "description": listing.description,
            "imageUrl": listing.image_url,
            "arv": listing.arv,
            "beds": getattr(listing, "beds", 0),
            "baths": getattr(listing, "baths", 0),
            "sqft": listing.square_footage,
            "approved": listing.approved,
        })

    return ListingRead.from_orm(listing)

# -------------------------
# ADMIN: GET PENDING LISTINGS
# -------------------------
@router.get("/admin/listings", response_model=List[ListingRead])
async def get_pending_listings(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")

    result = await db.execute(select(Listing).where(Listing.approved == False))
    listings = result.scalars().all()
    return [ListingRead.from_orm(l) for l in listings]

@router.delete("/{listing_id}")
async def delete_listing(
    listing_id: int,
    user_id: int = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    # 1️⃣ Fetch listing
    result = await session.execute(
        select(Listing).where(Listing.id == listing_id)
    )
    listing = result.scalar_one_or_none()

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")

    if listing.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # 2️⃣ Fetch associated images
    result = await session.execute(
        select(ListingImage).where(ListingImage.listing_id == listing_id)
    )
    images = result.scalars().all()

    # 3️⃣ Delete images from Supabase
    for img in images:
        # Extract file name from URL
        file_path = img.url.split("/")[-1].split("?")[0]
        supabase.storage.from_("listing-images").remove([file_path])

    # 4️⃣ Delete listing (CASCADE deletes images in DB)
    await session.delete(listing)
    await session.commit()

    return {"message": "Listing and images deleted successfully"}
    
    # WebSocket endpoint for buyer feed
@router.websocket("/ws/listings")
async def listings_ws(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()  # keep connection alive
    except Exception:
        manager.disconnect(websocket)

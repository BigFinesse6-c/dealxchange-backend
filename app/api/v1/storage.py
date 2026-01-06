from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.supabase import supabase
from app.utils.security import verify_access_token
from app.models.user import UserRole
from app.models.listing import Listing, ListingImage
from app.db.database import AsyncSession
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

bearer_scheme = HTTPBearer()
router = APIRouter(prefix="/storage", tags=["Storage"])

async def get_current_user(token: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    user_id = verify_access_token(token.credentials)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id

@router.post("/upload/{listing_id}")
async def upload_images(
    listing_id: int,
    files: list[UploadFile] = File(...),
    user_id: int = Depends(get_current_user),
    session: AsyncSession = Depends()
):
    # Verify listing ownership
    result = await session.execute(select(Listing).where(Listing.id == listing_id))
    listing = result.scalar_one_or_none()
    if not listing or listing.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    urls = []
    for file in files:
        ext = file.filename.split(".")[-1]
        key = f"{uuid.uuid4()}.{ext}"
        resp = supabase.storage.from_("listing-images").upload(key, await file.read())
        if resp.get("error"):
            raise HTTPException(status_code=400, detail=resp["error"]["message"])
        public_url = supabase.storage.from_("listing-images").create_signed_url(key, 3600)
        urls.append(public_url["signedURL"])
        # Save to DB
        img = ListingImage(listing_id=listing.id, url=public_url["signedURL"])
        session.add(img)

    await session.commit()
    return {"urls": urls}

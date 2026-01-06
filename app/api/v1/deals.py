from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from app.core.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.models.deal import Deal, DealStatus
from app.schemas.deal import DealCreate

router = APIRouter()

@router.post("/deals/request")
async def request_deal(
    deal_in: DealCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    deal = Deal(
        listing_id=deal_in.listing_id,
        buyer_id=current_user.id,
        status=DealStatus.REQUESTED,
        intro_fee_paid=True,  # for now
    )
    db.add(deal)
    await db.commit()
    return {"success": True}

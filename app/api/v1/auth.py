from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.db.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserRead, UserLogin, Token
from app.core.security import hash_password, verify_password, create_access_token
from app.core.auth import get_current_user

router = APIRouter()

# -------------------------
# Register / Signup
# -------------------------
# app/api/v1/auth.py (or wherever your signup endpoint is)
@router.post("/signup", response_model=UserRead)
async def signup(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_in.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # ✅ Only admins are auto-approved
    new_user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role or UserRole.buyer,
        approved=True,
        is_active=True #(user_in.role == UserRole.admin)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# -------------------------
# Login
# -------------------------
@router.post("/login", response_model=Token)
async def login(user_in: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_in.email))
    user = result.scalars().first()

    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    #if not user.approved:
        #raise HTTPException(status_code=403, detail="Account pending admin approval")

    access_token = create_access_token(user_id=user.id, role=user.role.value)
    return {"access_token": access_token, "token_type": "bearer"}

# -------------------------
# Current logged-in user
# -------------------------
@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


# -------------------------
# Admin-only: Get pending users
# -------------------------
@router.get("/admin/pending-users", response_model=List[UserRead])
async def get_pending_users(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only"
        )

    result = await db.execute(
        select(User).where(
            User.approved.is_(False),
            User.is_admin == False
        )
    )
    return result.scalars().all()


# -------------------------
# Admin-only: Approve user
# -------------------------
@router.patch("/admin/users/{user_id}/approve", response_model=UserRead)
async def approve_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.approved = True
    await db.commit()
    await db.refresh(user)
    return user
    
#@router.post("/deals/request")
#async def request_deal(
    #deal_in: DealCreate,
    #current_user: User = Depends(get_current_user),
    #db: AsyncSession = Depends(get_db),
#):
    #deal = Deal(
        #listing_id=deal_in.listing_id,
        #buyer_id=current_user.id,
        #status=DealStatus.REQUESTED,
        #intro_fee_paid=True,  # for now
    #)
    #db.add(deal)
    #await db.commit()
    #return {"success": True}

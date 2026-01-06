import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select

from app.db.database import engine, Base
from app.models.user import User
from app.models.listing import Listing
from app.core.security import hash_password


async def seed_admin(db):
    admin = User(
        email="admin@dealxchange.com",
        hashed_password=hash_password("admin123"),
        full_name="Local Admin",
        role="admin",
        is_admin=True,
        approved=True,
        is_active=True,
        is_verified_email=True,
    )
    db.add(admin)
    await db.commit()

async def seed():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session() as session:

        users = [
            ("admin@dealxchange.com", "admin123", "admin", True),
            ("seller@dealxchange.com", "seller123", "seller", True),
            ("buyer@dealxchange.com", "buyer123", "buyer", False),
            ("wholesaler@dealxchange.com", "wholesaler123", "wholesaler", True),
        ]

        for email, password, role, approved in users:
            session.add(User(
                email=email,
                hashed_password=hash_password(password),
                role=role,
                approved=approved,
                is_active=True,
                is_admin=(role == "admin"),
                is_verified_email=True
            ))

        await session.commit()

        # Seller listings
        seller = (await session.execute(
            select(User).where(User.email == "seller@dealxchange.com")
        )).scalar_one()

        session.add_all([
            Listing(
                title="Fix & Flip Opportunity",
                address="4320 Maple Ave",
                zip_code="72204",
                square_footage=1100,
                price=40000,
                owner_id=seller.id,
                approved=False
            )
        ])

        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed())

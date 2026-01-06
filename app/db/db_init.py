# app/db_init.py
import asyncio
from app.db.database import Base, engine, get_db

async def init_db():
    async with engine.begin() as conn:
        # Drop all tables (optional, useful for testing)
        # await conn.run_sync(Base.metadata.drop_all)

        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Database initialized successfully!")

if __name__ == "__main__":
    asyncio.run(init_db())


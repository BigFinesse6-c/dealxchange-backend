from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.db.base_class import Base
from app.core.config import settings

# Convert DATABASE_URL to async URL
ASYNC_DATABASE_URL = settings.DATABASE_URL

# Async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # optional, good for debugging
    pool_pre_ping=True,
    connect_args={"statement_cache_size": 0,},
)

# Async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency for FastAPI
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

# Async function to create tables (run once for initial setup)
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

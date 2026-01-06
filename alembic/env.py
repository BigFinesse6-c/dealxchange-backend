from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy import engine_from_config
from sqlalchemy import create_engine
from alembic import context
from app.db.base_class import Base
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine

# Alembic Config object
config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Async engine for migrations
DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool, connect_args={"statement_cache_size": 0},)

def run_migrations_offline():
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())

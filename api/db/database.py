"""
SQLAlchemy Async Database Setup
Provides async engine, session maker, and database dependencies for FastAPI
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator

# SQLite database URL (uses aiosqlite for async operations)
DATABASE_URL = "sqlite+aiosqlite:///./news_cache.db"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Create async session maker
async_session_maker = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Base class for ORM models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides database sessions to FastAPI endpoints.
    Handles commit/rollback automatically.
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    Initialize database tables.
    Should be called on application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

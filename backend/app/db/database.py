from typing import AsyncIterator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings

async_engine = create_async_engine(url=settings.pg_dns, pool_pre_ping=True, echo=False)

AsyncSessionLocal = async_sessionmaker(bind=async_engine, autoflush=False, future=True)


async def get_session() -> AsyncIterator[async_sessionmaker]:
    yield AsyncSessionLocal

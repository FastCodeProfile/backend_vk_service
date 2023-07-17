from __future__ import annotations

from typing import AsyncIterator, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, unique=True, primary_key=True
    )

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs) -> BaseModel:
        entry = cls(**kwargs)
        session.add(entry)
        await session.flush()
        return await cls.read_by_id(session, entry.id)

    @classmethod
    async def read_by_id(
        cls, session: AsyncSession, entry_id: int
    ) -> Optional[BaseModel]:
        stmt = select(cls).where(cls.id == entry_id)
        return await session.scalar(stmt.order_by(cls.id))

    @classmethod
    async def read_all(cls, session: AsyncSession) -> AsyncIterator[BaseModel]:
        stmt = select(cls)
        stream = await session.stream_scalars(stmt.order_by(cls.id))
        async for row in stream:
            yield row

    @classmethod
    async def delete(cls, session: AsyncSession, entry: BaseModel) -> None:
        if await cls.read_by_id(session=session, entry_id=entry.id):
            await session.delete(entry)
            await session.flush()

from __future__ import annotations

from datetime import datetime as dt
from typing import AsyncIterator, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Group(BaseModel):
    __tablename__ = "groups"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    bot_id: Mapped[int] = mapped_column(ForeignKey("bots.id"))
    group_id: Mapped[int] = mapped_column("group_id", Integer(), nullable=False)
    last_call = mapped_column("last_call", DateTime(), default=dt.now())

    async def update(self, session: AsyncSession) -> None:
        self.last_call = dt.now()
        await session.flush()
        await session.commit()

    @classmethod
    async def read_by_group_id(
        cls, session: AsyncSession, group_id: int
    ) -> Optional[Group]:
        stmt = select(cls).where(cls.group_id == group_id)
        return await session.scalar(stmt.order_by(cls.id))

    @classmethod
    async def read_all_with_id(
        cls, session: AsyncSession, start_with_id: int
    ) -> AsyncIterator[Group]:
        stmt = select(cls).where(cls.id > start_with_id)
        stream = await session.stream_scalars(stmt.order_by(cls.last_call))
        async for row in stream:
            yield row

    @classmethod
    async def read_all_me(
        cls, session: AsyncSession, user_id: int
    ) -> AsyncIterator[Group]:
        stmt = select(cls).where(cls.user_id == user_id)
        stream = await session.stream_scalars(stmt.order_by(cls.id))
        async for row in stream:
            yield row

    @classmethod
    async def read_all_by_bot_id(
        cls, session: AsyncSession, bot_id: int
    ) -> AsyncIterator[Group]:
        stmt = select(cls).where(cls.bot_id == bot_id)
        stream = await session.stream_scalars(stmt.order_by(cls.id))
        async for row in stream:
            yield row

    @classmethod
    async def create_group(
        cls, session: AsyncSession, user_id: int, bot_id: int, group_id: int
    ) -> Group:
        return await cls.create(
            session=session, user_id=user_id, bot_id=bot_id, group_id=group_id
        )

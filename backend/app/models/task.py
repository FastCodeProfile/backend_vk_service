from __future__ import annotations

from typing import AsyncIterator, Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String, and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Task(BaseModel):
    __tablename__ = "tasks"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    type_: Mapped[str] = mapped_column("type_", String(), nullable=True)
    item_id: Mapped[int] = mapped_column("item_id", Integer(), nullable=True)
    owner_id: Mapped[int] = mapped_column("owner_id", Integer(), nullable=False)
    completed: Mapped[bool] = mapped_column("completed", Boolean(), default=False)
    in_progress: Mapped[bool] = mapped_column("in_progress", Boolean(), default=False)
    amount: Mapped[int] = mapped_column("amount", Integer(), nullable=False)
    amount_done: Mapped[int] = mapped_column("amount_done", Integer(), default=0)
    last_entry_id: Mapped[int] = mapped_column("last_entry_id", Integer(), default=0)

    @classmethod
    async def read_all_pending(cls, session: AsyncSession) -> AsyncIterator[Task]:
        stmt = (
            select(cls)
            .where(cls.in_progress.is_(False))
            .where(cls.completed.is_(False))
        )
        stream = await session.stream_scalars(stmt.order_by(cls.id))
        async for row in stream:
            yield row

    @classmethod
    async def exists(
        cls, session: AsyncSession, type_: str, item_id: int, owner_id: int
    ) -> Optional[Task]:
        stmt = select(cls).where(
            and_(cls.type_ == type_, cls.item_id == item_id, cls.owner_id == owner_id)
        )
        return await session.scalar(stmt.order_by(cls.id))

    @classmethod
    async def create_task(
        cls,
        session: AsyncSession,
        user_id: int,
        amount: int,
        type_: str,
        item_id: int,
        owner_id: int,
    ) -> Task:
        return await cls.create(
            session=session,
            user_id=user_id,
            amount=amount,
            type_=type_,
            item_id=item_id,
            owner_id=owner_id,
        )

    async def update(
        self,
        session: AsyncSession,
        completed,
        in_progress,
        amount: int = None,
        amount_done: int = None,
        last_entry_id: int = None,
    ) -> None:
        self.completed = completed
        self.in_progress = in_progress
        self.amount = amount or self.amount
        self.amount_done = amount_done or self.amount_done
        self.last_entry_id = last_entry_id or self.last_entry_id
        await session.flush()

    @classmethod
    async def read_all_me(
        cls, session: AsyncSession, user_id: int
    ) -> AsyncIterator[Task]:
        stmt = select(cls).where(cls.user_id == user_id)
        stream = await session.stream_scalars(stmt.order_by(cls.completed))
        async for row in stream:
            yield row

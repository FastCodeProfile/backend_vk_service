from __future__ import annotations

from typing import AsyncIterator, Optional

from sqlalchemy import ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Bot(BaseModel):
    __tablename__ = "bots"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner_id: Mapped[int] = mapped_column("owner_id", Integer(), nullable=False)
    full_name: Mapped[int] = mapped_column("full_name", String(), nullable=False)
    login: Mapped[str] = mapped_column("login", String(), nullable=False)
    password: Mapped[str] = mapped_column("password", String(), nullable=False)
    user_agent: Mapped[str] = mapped_column("user_agent", String(), nullable=True)
    access_token: Mapped[str] = mapped_column("access_token", String(), nullable=False)

    @classmethod
    async def read_by_owner_id(
        cls, session: AsyncSession, owner_id: int
    ) -> Optional[Bot]:
        stmt = select(cls).where(cls.owner_id == owner_id)
        return await session.scalar(stmt.order_by(cls.id))

    @classmethod
    async def read_all_me(
        cls, session: AsyncSession, user_id: int
    ) -> AsyncIterator[Bot]:
        stmt = select(cls).where(cls.user_id == user_id)
        stream = await session.stream_scalars(stmt.order_by(cls.id))
        async for row in stream:
            yield row

    @classmethod
    async def create_bot(
        cls,
        session: AsyncSession,
        user_id: int,
        owner_id: int,
        full_name: str,
        login: str,
        password: str,
        user_agent: str,
        access_token: str,
    ) -> Bot:
        return await cls.create(
            session=session,
            user_id=user_id,
            owner_id=owner_id,
            full_name=full_name,
            login=login,
            password=password,
            user_agent=user_agent,
            access_token=access_token,
        )

    async def update(self, session: AsyncSession, password, access_token) -> None:
        self.password = password
        self.access_token = access_token
        await session.flush()

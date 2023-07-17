from __future__ import annotations

from hashlib import md5

from sqlalchemy import Boolean, Float, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"
    balance: Mapped[float] = mapped_column("balance", Float(), default=0)
    username: Mapped[str] = mapped_column(
        "username", String(), nullable=False, unique=True
    )
    password: Mapped[str] = mapped_column("password", String(), nullable=False)
    access_token: Mapped[str] = mapped_column("access_token", String(), nullable=False)
    is_superuser: Mapped[bool] = mapped_column("is_superuser", Boolean(), default=False)

    @classmethod
    async def create_user(
        cls, session: AsyncSession, username: str, password: str
    ) -> User:
        access_token = md5(bytes(f"{username}_{password}", "utf-8")).hexdigest()
        return await cls.create(
            session, username=username, password=password, access_token=access_token
        )

    @classmethod
    async def read_by_access_token(
        cls, session: AsyncSession, access_token: str
    ) -> User:
        stmt = select(cls).where(cls.access_token == access_token)
        return await session.scalar(stmt.order_by(cls.id))

    @classmethod
    async def read_by_username(cls, session: AsyncSession, username: str) -> User:
        stmt = select(cls).where(cls.username == username)
        return await session.scalar(stmt.order_by(cls.id))

    async def update(self, session: AsyncSession, balance) -> None:
        self.balance = balance
        await session.flush()

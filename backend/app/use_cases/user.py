from typing import AsyncIterator

from app import models, schemas

from .base import UseCases


class UserCreate(UseCases):
    async def execute(self, username: str, password: str) -> schemas.UserSchema:
        async with self.async_session.begin() as session:
            entry = await models.User.read_by_username(session, username)
            if not entry:
                entry = await models.User.create_user(session, username, password)
                return schemas.UserSchema.from_orm(entry)


class UserRead(UseCases):
    async def by_access_token(self, access_token: str) -> schemas.UserSchema:
        async with self.async_session() as session:
            entry = await models.User.read_by_access_token(session, access_token)
            if entry:
                return schemas.UserSchema.from_orm(entry)

    async def by_username(self, username) -> schemas.UserSchema:
        async with self.async_session() as session:
            entry = await models.User.read_by_username(session, username)
            if entry:
                return schemas.UserSchema.from_orm(entry)

    async def by_id(self, user_id: int) -> schemas.UserSchema:
        async with self.async_session() as session:
            entry = await models.User.read_by_id(session, user_id)
            if entry:
                return schemas.UserSchema.from_orm(entry)


class UserReadAll(UseCases):
    async def execute(self) -> AsyncIterator[schemas.UserSchema]:
        async with self.async_session() as session:
            async for entry in models.User.read_all(session):
                yield schemas.UserSchema.from_orm(entry)


class UserUpdate(UseCases):
    async def execute(self, user_id: int, balance: float) -> schemas.UserSchema:
        async with self.async_session.begin() as session:
            entry = await models.User.read_by_id(session, user_id)
            if entry:
                await entry.update(session, balance)
                await session.refresh(entry)
                return schemas.UserSchema.from_orm(entry)

from typing import AsyncIterator

from app import models, schemas

from .base import UseCases


class BotCreate(UseCases):
    async def execute(
        self,
        user_id: int,
        owner_id: int,
        full_name: str,
        login: str,
        password: str,
        user_agent: str,
        access_token: str,
    ) -> schemas.BotSchema:
        async with self.async_session.begin() as session:
            entry = await models.Bot.read_by_owner_id(session, owner_id=owner_id)
            if entry:
                await entry.update(
                    session=session, password=password, access_token=access_token
                )
            else:
                entry = await models.Bot.create_bot(
                    session,
                    user_id=user_id,
                    owner_id=owner_id,
                    full_name=full_name,
                    login=login,
                    password=password,
                    user_agent=user_agent,
                    access_token=access_token,
                )
            return schemas.BotSchema.from_orm(entry)


class BotRead(UseCases):
    async def execute(self, entry_id: int) -> schemas.BotSchema:
        async with self.async_session() as session:
            entry = await models.Bot.read_by_id(session, entry_id=entry_id)
            if entry:
                return schemas.BotSchema.from_orm(entry)


class BotReadAll(UseCases):
    async def execute(self) -> AsyncIterator[schemas.BotSchema]:
        async with self.async_session() as session:
            async for entry in models.Bot.read_all(session):
                yield schemas.BotSchema.from_orm(entry)

    async def read_all_me(self, user_id: int) -> AsyncIterator[schemas.BotSchema]:
        async with self.async_session() as session:
            async for entry in models.Bot.read_all_me(session, user_id=user_id):
                yield schemas.BotSchema.from_orm(entry)


class BotDelete(UseCases):
    async def execute(self, entry_id: int) -> None:
        async with self.async_session.begin() as session:
            entry = await models.Bot.read_by_id(session, entry_id=entry_id)
            if entry:
                await models.Bot.delete(session, entry)


class BotUpdate(UseCases):
    async def execute(
        self,
        entry_id: int,
        password: str,
        access_token: str,
    ) -> schemas.BotSchema:
        async with self.async_session.begin() as session:
            entry = await models.Bot.read_by_id(session=session, entry_id=entry_id)
            if entry:
                await entry.update(
                    session,
                    password=password,
                    access_token=access_token,
                )
                await session.refresh(entry)
                return schemas.BotSchema.from_orm(entry)

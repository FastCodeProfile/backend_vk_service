from typing import AsyncIterator

from app import models, schemas

from .base import UseCases


class GroupCreate(UseCases):
    async def execute(
        self, user_id: int, bot_id: int, group_id: int
    ) -> schemas.GroupSchema:
        async with self.async_session.begin() as session:
            entry = await models.Group.read_by_group_id(session, group_id)
            if not entry:
                entry = await models.Group.create_group(
                    session, user_id=user_id, bot_id=bot_id, group_id=group_id
                )
            return schemas.GroupSchema.from_orm(entry)


class GroupRead(UseCases):
    async def execute(self, entry_id) -> schemas.GroupSchema:
        async with self.async_session() as session:
            entry = await models.Group.read_by_id(session, entry_id=entry_id)
            if entry:
                return schemas.GroupSchema.from_orm(entry)


class GroupUpdate(UseCases):
    async def execute(self, entry_id):
        async with self.async_session() as session:
            entry = await models.Group.read_by_id(session, entry_id=entry_id)
            if entry:
                await entry.update(session)
                await session.refresh(entry)


class GroupReadAll(UseCases):
    async def execute(self) -> AsyncIterator[schemas.GroupSchema]:
        async with self.async_session() as session:
            async for entry in models.Group.read_all(session=session):
                yield schemas.GroupSchema.from_orm(entry)

    async def read_all_me(self, user_id: int) -> AsyncIterator[schemas.GroupSchema]:
        async with self.async_session() as session:
            async for entry in models.Group.read_all_me(
                session=session, user_id=user_id
            ):
                yield schemas.GroupSchema.from_orm(entry)

    async def by_bot_id(self, bot_id: int) -> AsyncIterator[schemas.GroupSchema]:
        async with self.async_session() as session:
            async for entry in models.Group.read_all_by_bot_id(
                session=session, bot_id=bot_id
            ):
                yield schemas.GroupSchema.from_orm(entry)

    async def by_start_with_id(
        self, start_with_id: int
    ) -> AsyncIterator[schemas.GroupSchema]:
        async with self.async_session() as session:
            async for entry in models.Group.read_all_with_id(
                session=session, start_with_id=start_with_id
            ):
                yield schemas.GroupSchema.from_orm(entry)


class GroupDelete(UseCases):
    async def execute(self, entry_id: int) -> None:
        async with self.async_session.begin() as session:
            entry = await models.Group.read_by_id(session, entry_id=entry_id)
            if entry:
                await models.Group.delete(session, entry=entry)

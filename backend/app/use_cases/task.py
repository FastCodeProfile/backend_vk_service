from typing import AsyncIterator

from app import models, schemas

from .base import UseCases


class TaskCreate(UseCases):
    async def execute(
        self, user_id: int, amount: int, type_: str, item_id: int, owner_id: int
    ) -> schemas.TaskSchema:
        async with self.async_session.begin() as session:
            entry = await models.Task.exists(
                session=session, type_=type_, item_id=item_id, owner_id=owner_id
            )
            if entry:
                amount += entry.amount
                await entry.update(
                    session=session,
                    completed=False,
                    in_progress=False,
                    amount=amount,
                )
            else:
                entry = await models.Task.create_task(
                    session=session,
                    user_id=user_id,
                    amount=amount,
                    type_=type_,
                    item_id=item_id,
                    owner_id=owner_id,
                )
            return schemas.TaskSchema.from_orm(entry)


class TaskReadAll(UseCases):
    async def execute(self) -> AsyncIterator[schemas.TaskSchema]:
        async with self.async_session() as session:
            async for entry in models.Task.read_all(session=session):
                yield schemas.TaskSchema.from_orm(entry)

    async def read_all_me(self, user_id: int) -> AsyncIterator[schemas.TaskSchema]:
        async with self.async_session() as session:
            async for entry in models.Task.read_all_me(
                session=session, user_id=user_id
            ):
                yield schemas.TaskSchema.from_orm(entry)

    async def pending(self) -> AsyncIterator[schemas.TaskSchema]:
        async with self.async_session() as session:
            async for entry in models.Task.read_all_pending(session=session):
                yield schemas.TaskSchema.from_orm(entry)


class TaskUpdate(UseCases):
    async def execute(
        self,
        entry_id: int,
        completed: bool,
        in_progress: bool,
        amount: int = None,
        amount_done: int = None,
        last_entry_id: int = None,
    ) -> schemas.TaskSchema:
        async with self.async_session.begin() as session:
            entry = await models.Task.read_by_id(session=session, entry_id=entry_id)
            await entry.update(
                session,
                completed=completed,
                in_progress=in_progress,
                amount=amount or entry.amount,
                amount_done=amount_done or entry.amount_done,
                last_entry_id=last_entry_id or entry.last_entry_id,
            )
            await session.refresh(entry)
            return schemas.TaskSchema.from_orm(entry)


class TaskDelete(UseCases):
    async def execute(self, entry_id: int) -> None:
        async with self.async_session.begin() as session:
            entry = await models.Task.read_by_id(session=session, entry_id=entry_id)
            await models.Task.delete(session, entry)

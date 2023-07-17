import asyncio

from loguru import logger

from app import schemas, use_cases
from app.core.vk_api import API, APIError


async def execution_tasks(ctx, entry: schemas.TaskSchema):
    api = API()
    logger.info(f"Выполняю задачу №{entry.id}.")
    await use_cases.TaskUpdate(ctx["session"]).execute(
        entry_id=entry.id, completed=False, in_progress=True
    )
    async for group in use_cases.GroupReadAll(ctx["session"]).by_start_with_id(
        start_with_id=entry.last_entry_id
    ):
        await use_cases.GroupUpdate(ctx["session"]).execute(group.id)
        bot = await use_cases.BotRead(ctx["session"]).execute(group.bot_id)
        api.token = bot.access_token
        api.ua = bot.user_agent
        try:
            await api.request(
                "wall.repost",
                group_id=group.group_id,
                object=f"wall{entry.owner_id}_{entry.item_id}",
            )
            entry.amount_done += 1
            entry.last_entry_id = group.id

        except APIError as err:
            logger.info(f"Ошибка №{err.code} при выполнении задачи: {err.error}")
            if err.code in [5, 17]:
                async for bot_group in use_cases.GroupReadAll(ctx["session"]).by_bot_id(
                    bot.id
                ):
                    await use_cases.GroupDelete(ctx["session"]).execute(bot_group.id)
                await use_cases.BotDelete(ctx["session"]).execute(bot.id)
                logger.info(
                    f"Аккаунт и его группы удалены из базы данные, аккаунт. - {bot}"
                )
                return await execution_tasks(ctx, entry)
        finally:
            if entry.amount <= entry.amount_done:
                logger.success(f"Задача №{entry.id}. Выполнено.")
                await use_cases.TaskUpdate(ctx["session"]).execute(
                    entry_id=entry.id,
                    completed=True,
                    in_progress=False,
                    amount_done=entry.amount_done,
                    last_entry_id=group.id,
                )
                return
            else:
                await use_cases.TaskUpdate(ctx["session"]).execute(
                    entry_id=entry.id,
                    completed=False,
                    in_progress=True,
                    amount_done=entry.amount_done,
                    last_entry_id=group.id,
                )

        await use_cases.TaskUpdate(ctx["session"]).execute(
            entry_id=entry.id,
            completed=False,
            in_progress=False,
            amount_done=entry.amount_done,
            last_entry_id=group.id,
        )


async def run_tasks_pending(ctx):
    tasks = []
    async for entry in use_cases.TaskReadAll(ctx["session"]).pending():
        task = asyncio.create_task(execution_tasks(ctx, entry))
        tasks.append(task)
    await asyncio.gather(*tasks)

from loguru import logger

from app import use_cases
from app.core.vk_api import API, APIError


async def creating_groups(ctx):
    api = API()
    logger.info("Выполняю задачу, создание групп.")
    async for bot in use_cases.BotReadAll(ctx["session"]).execute():
        api.token = bot.access_token
        api.ua = bot.user_agent
        groups = use_cases.GroupReadAll(ctx["session"]).by_bot_id(bot_id=bot.id)
        if 100 <= len([x async for x in groups]):
            continue
        try:
            group_id = await api.create_group()
            await use_cases.GroupCreate(ctx["session"]).execute(
                user_id=bot.user_id, bot_id=bot.id, group_id=group_id
            )
        except APIError as err:
            logger.info(
                f"Ошибка №{err.code} при выполнении задачи, создание групп: {err.error}"
            )
            if err.code in [5, 17]:
                async for group in groups:
                    await use_cases.GroupDelete(ctx["session"]).execute(group.id)
                await use_cases.BotDelete(ctx["session"]).execute(bot.id)
                logger.info(
                    f"Аккаунт и его группы удалены из базы данные, аккаунт. - {bot}"
                )

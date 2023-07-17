from loguru import logger

from app import use_cases
from app.core.config import settings


async def income(ctx):
    logger.info("Выполняю задачу, отправка дохода.")
    async for user in use_cases.UserReadAll(ctx["session"]).execute():
        total_accounts = len(
            [
                _
                async for _ in use_cases.BotReadAll(ctx["session"]).read_all_me(
                    user_id=user.id
                )
            ]
        )
        await use_cases.UserUpdate(ctx["session"]).execute(
            user_id=user.id, balance=(total_accounts * settings.INCOME) + user.balance
        )
        logger.success(
            f"Пользователь №{user.id} получил {total_accounts * settings.INCOME}руб."
        )

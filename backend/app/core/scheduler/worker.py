from arq import cron

from app.core.config import settings
from app.db import AsyncSessionLocal

from .tasks import group, income, task


async def startup(ctx):
    ctx["session"] = AsyncSessionLocal


class WorkerSettings:
    redis_settings = settings.redis
    on_startup = startup
    functions = [task.execution_tasks]
    cron_jobs = [
        cron(task.run_tasks_pending, second=0),
        cron(group.creating_groups, minute=0),
        cron(income.income, hour=0, minute=0),
    ]

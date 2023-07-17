from typing import Annotated

from fastapi import APIRouter, Depends

from app import schemas, use_cases
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.get("/all", response_model=schemas.StatisticsSchema)
async def read_all(
    group_read_all: Annotated[use_cases.GroupReadAll, Depends(use_cases.GroupReadAll)],
    task_read_all: Annotated[use_cases.TaskReadAll, Depends(use_cases.TaskReadAll)],
    bot_read_all: Annotated[use_cases.BotReadAll, Depends(use_cases.BotReadAll)],
):
    total_tasks = len([entry async for entry in task_read_all.execute()])
    total_groups = len([entry async for entry in group_read_all.execute()])
    total_bots = len([entry async for entry in bot_read_all.execute()])
    speed_in_day = total_bots * 24
    return schemas.StatisticsSchema(
        speed_in_day=speed_in_day,
        total_tasks=total_tasks,
        total_groups=total_groups,
        total_bots=total_bots,
    )


@router.get("/me", response_model=schemas.StatisticsMe)
async def read_me(
    current_user: Annotated[schemas.UserSchema, Depends(deps.get_current_user)],
    group_read_all: Annotated[use_cases.GroupReadAll, Depends(use_cases.GroupReadAll)],
    task_read_all: Annotated[use_cases.TaskReadAll, Depends(use_cases.TaskReadAll)],
    bot_read_all: Annotated[use_cases.BotReadAll, Depends(use_cases.BotReadAll)],
):
    user_id = current_user.id
    total_tasks = len(
        [entry async for entry in task_read_all.read_all_me(user_id=user_id)]
    )
    total_groups = len(
        [entry async for entry in group_read_all.read_all_me(user_id=user_id)]
    )
    total_bots = len(
        [entry async for entry in bot_read_all.read_all_me(user_id=user_id)]
    )
    income_in_day = total_bots * settings.INCOME
    speed_in_day = total_bots * 24
    return schemas.StatisticsMe(
        income_in_day=income_in_day,
        speed_in_day=speed_in_day,
        total_tasks=total_tasks,
        total_groups=total_groups,
        total_bots=total_bots,
    )

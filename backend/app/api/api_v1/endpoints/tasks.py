from typing import Annotated

from arq import create_pool
from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from app import schemas, use_cases
from app.api import deps
from app.core.config import settings
from app.core.vk_api import url_to_kwargs

router = APIRouter()


@router.post("/", response_model=schemas.TaskSchema)
async def create(
    data: schemas.TaskCreate,
    current_user: Annotated[schemas.UserSchema, Depends(deps.get_current_user)],
    task_create: Annotated[use_cases.TaskCreate, Depends(use_cases.TaskCreate)],
    user_update: Annotated[use_cases.UserUpdate, Depends(use_cases.UserUpdate)],
):
    price = data.amount * settings.PRICE
    if current_user.balance >= price:
        kwargs = await url_to_kwargs(data.link)
        if kwargs:
            if kwargs.get("type_") == "post":
                logger.info(f"Создана новая задача, накрутка репостов. - {data}")
                await user_update.execute(
                    user_id=current_user.id, balance=current_user.balance - price
                )
                redis = await create_pool(settings.redis)
                entry = await task_create.execute(
                    user_id=current_user.id, amount=data.amount, **kwargs
                )
                await redis.enqueue_job("execution_tasks", entry)
                return entry
            else:
                raise HTTPException(
                    status_code=404, detail="Ссылка должна вести на пост."
                )
        else:
            raise HTTPException(status_code=404, detail="Пост не найден.")
    else:
        raise HTTPException(status_code=404, detail="У вас не достаточно средств.")


@router.get("/", response_model=schemas.TaskReadAll)
async def read_all(
    current_user: Annotated[schemas.UserSchema, Depends(deps.get_current_user)],
    task_read_all: Annotated[use_cases.TaskReadAll, Depends(use_cases.TaskReadAll)],
):
    list_task = [
        entry async for entry in task_read_all.read_all_me(user_id=current_user.id)
    ]
    return schemas.TaskReadAll(amount=len(list_task), list=list_task)

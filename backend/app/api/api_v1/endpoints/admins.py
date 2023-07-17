from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app import schemas, use_cases
from app.api import deps

router = APIRouter()


@router.put("/balance/add/{user_id}", response_model=schemas.UserSchema)
async def balance_add(
    user_id: int,
    data: schemas.UserUpdate,
    current_user: Annotated[schemas.UserSchema, Depends(deps.get_current_user)],
    user_update: Annotated[use_cases.UserUpdate, Depends(use_cases.UserUpdate)],
    user_read: Annotated[use_cases.UserRead, Depends(use_cases.UserRead)],
):
    if current_user.is_superuser:
        user = await user_read.by_id(user_id)
        return await user_update.execute(user_id, user.balance + data.balance)
    else:
        raise HTTPException(status_code=403, detail="У вас нет прав администратора.")

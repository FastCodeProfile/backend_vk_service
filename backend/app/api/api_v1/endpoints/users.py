from secrets import compare_digest
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas, use_cases
from app.api import deps

router = APIRouter()


@router.post("/sign-up", response_model=schemas.UserTokenSchema)
async def sign_up(
    data: schemas.UserCreate,
    user_create: Annotated[use_cases.UserCreate, Depends(use_cases.UserCreate)],
):
    user = await user_create.execute(data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=401, detail="Такой пользователь уже зарегистрирован"
        )
    return schemas.UserTokenSchema(access_token=user.access_token)


@router.post("/sign-in", response_model=schemas.UserTokenSchema)
async def sign_in(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_read: Annotated[use_cases.UserRead, Depends(use_cases.UserRead)],
):
    user = await user_read.by_username(data.username)
    if not user or not compare_digest(data.password, user.password):
        raise HTTPException(
            status_code=401, detail="Неверное имя пользователя или пароль"
        )
    return schemas.UserTokenSchema(access_token=user.access_token)


@router.get("/me", response_model=schemas.UserMe)
async def me(
    current_user: Annotated[schemas.UserSchema, Depends(deps.get_current_user)]
):
    return schemas.UserMe(**current_user.dict())

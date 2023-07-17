from typing import Annotated

from fake_useragent import UserAgent
from fastapi import APIRouter, Depends, HTTPException

from app import schemas, use_cases
from app.api import deps
from app.core.vk_api import API, APIError

router = APIRouter()


@router.post("/", response_model=schemas.BotSchema)
async def create(
    data: schemas.BotCreate,
    current_user: Annotated[schemas.UserSchema, Depends(deps.get_current_user)],
    account_create: Annotated[use_cases.BotCreate, Depends(use_cases.BotCreate)],
):
    ua = UserAgent().random
    try:
        api = API(data.access_token, ua)
        bot = await api.get_bot_info()
        data = await api.change_password(data)
        return await account_create.execute(
            user_id=current_user.id,
            owner_id=bot["id"],
            full_name=f"{bot['first_name']} {bot['last_name']}",
            login=data.login,
            password=data.password,
            user_agent=ua,
            access_token=data.access_token,
        )
    except APIError as err:
        raise HTTPException(status_code=404, detail=err.error)


@router.get("/", response_model=schemas.BotReadAll)
async def read_all(
    current_user: Annotated[schemas.UserSchema, Depends(deps.get_current_user)],
    account_read_all: Annotated[use_cases.BotReadAll, Depends(use_cases.BotReadAll)],
):
    user_id = current_user.id
    list_account = [entry async for entry in account_read_all.read_all_me(user_id)]
    return schemas.BotReadAll(amount=len(list_account), list=list_account)

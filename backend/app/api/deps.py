from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app import use_cases
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/users/sign-in")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    use_case: Annotated[use_cases.UserRead, Depends(use_cases.UserRead)],
):
    user = await use_case.by_access_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен недействителен",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

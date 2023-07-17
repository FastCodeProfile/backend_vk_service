from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db import get_session

AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]


class UseCases:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

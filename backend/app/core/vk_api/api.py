import random
from string import ascii_letters

from faker import Faker
from httpx import AsyncClient
from loguru import logger

from app import schemas

from .exceptions import APIError

fake = Faker("ru_RU")


class API:
    _host = "https://api.vk.com/method/"

    def __init__(self, token: str = None, ua: str = None) -> None:
        self.token = token
        self.ua = ua

    async def request(self, method: str, **params) -> dict | list:
        params["v"] = 5.131
        headers = {"Authorization": f"Bearer {self.token}", "User-Agent": self.ua}
        if not self.ua:
            headers.pop("User-Agent")
        async with AsyncClient(headers=headers) as client:
            response = await client.get(self._host + method, params=params)
            if response.status_code == 200:
                response_json = response.json()
                if "error" not in response_json:
                    logger.success(response_json["response"])
                    return response_json["response"]
                else:
                    logger.error(f'Ошибка: {response_json["error"]}')
                    raise APIError(
                        code=response_json["error"]["error_code"],
                        error=response_json["error"]["error_msg"],
                    )
            else:
                raise APIError(
                    code=response.status_code, error="Неожиданный статус код"
                )

    async def change_password(self, data: schemas.BotCreate):
        new_password = "".join([random.choice(ascii_letters) for _ in range(10)])
        data.access_token = (
            await self.request(
                "account.changePassword",
                old_password=data.password,
                new_password=new_password,
            )
        )["token"]
        data.password = new_password
        return data

    async def get_bot_info(self) -> dict:
        users = await self.request("users.get")
        return users[0]

    async def get_group_id(self) -> int:
        users = await self.request("groups.getById")
        return users[0]["id"]

    async def is_closed(self, user_id: int) -> bool:
        result = await self.request("users.get", user_ids=user_id)
        if result:
            return result[0]["is_closed"]
        else:
            return True

    async def create_group(self) -> int:
        title = f"{fake.first_name()} {fake.last_name()}"
        result = await self.request(
            "groups.create", title=title, type="public", subtype=2
        )
        return result["id"]

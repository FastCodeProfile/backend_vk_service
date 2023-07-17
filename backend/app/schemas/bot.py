from pydantic import BaseModel


class BotSchema(BaseModel):
    id: int
    user_id: int
    owner_id: int
    full_name: str
    login: str
    password: str
    user_agent: str
    access_token: str

    class Config:
        orm_mode = True


class BotCreate(BaseModel):
    login: str
    password: str
    access_token: str


class BotReadAll(BaseModel):
    amount: int
    list: list[BotSchema]

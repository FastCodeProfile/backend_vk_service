from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    balance: float
    username: str
    password: str
    access_token: str
    is_superuser: bool

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    balance: float


class UserMe(UserSchema):
    pass


class UserTokenSchema(BaseModel):
    access_token: str
    token_type: str = "Bearer"

    class Config:
        allow_population_by_field_name = True

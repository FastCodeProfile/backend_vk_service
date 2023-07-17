from pydantic import BaseModel, Field


class GroupSchema(BaseModel):
    id: int
    user_id: int
    bot_id: int
    group_id: int

    class Config:
        orm_mode = True


class GroupCreate(BaseModel):
    bot_id: int = Field(0)
    group_id: int = Field(0)


class GroupReadAll(BaseModel):
    list_group: list[GroupSchema]

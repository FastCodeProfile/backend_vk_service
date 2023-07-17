from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: int
    user_id: int
    type_: str
    item_id: int
    owner_id: int
    completed: bool
    in_progress: bool
    amount: int
    amount_done: int
    last_entry_id: int

    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    link: str
    amount: int


class TaskReadAll(BaseModel):
    amount: int
    list: list[TaskSchema]

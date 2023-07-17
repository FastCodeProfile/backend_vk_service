from pydantic import BaseModel


class StatisticsSchema(BaseModel):
    speed_in_day: int
    total_tasks: int
    total_groups: int
    total_bots: int


class StatisticsMe(StatisticsSchema):
    income_in_day: float

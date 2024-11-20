from pydantic import BaseModel


class UserHabitData(BaseModel):
    user_id: int
    name: str
    description: str

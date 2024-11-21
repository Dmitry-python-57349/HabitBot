from pydantic import BaseModel


class UserHabitData(BaseModel):
    user_id: int
    name: str
    description: str


class UserData(BaseModel):
    user_id: int
    username: str
    firstname: str
    lastname: str

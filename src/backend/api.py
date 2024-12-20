from fastapi import FastAPI, Body
from fastapi.routing import APIRoute

from src.backend.pydantic_models import UserHabitData, UserData
from src.backend.sql_core import AsyncORM
from src.notification.notification import lifespan

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def index():
    result = dict()
    for route in app.routes:
        if not isinstance(route, APIRoute):
            continue
        result[route.path] = {
            "name": route.name,
            "methods": route.methods,
        }
    return {"API": result}


@app.post("/add_user/")
async def add_user(user: UserData):
    user_id = await AsyncORM.add_user(user=user)
    return {"message": f"<User: {user_id}> created!"}


@app.get("/get_habit_marks/")
async def get_habits(habit_id: int):
    habit_marks = await AsyncORM.get_habit_marks(habit_id=habit_id)
    return {"data": habit_marks}


@app.get("/get_habits/")
async def get_habits(user_id: int):
    habits = await AsyncORM.get_habits(user_id=user_id)
    return {"data": habits}


@app.post("/add_habit/")
async def add_habit(data: UserHabitData):
    habit_id = await AsyncORM.add_habit(data=data)
    return {"message": f"<Habit: {habit_id}> has been created!"}


@app.put("/edit_habit/")
async def edit_habit(data=Body()):
    await AsyncORM.edit_habit(**data)
    return {"message": f"Habit edited!"}


@app.delete("/delete_habit/")
async def delete_habit(data=Body()):
    await AsyncORM.delete_habit(habit_id=data["habit_id"])
    return {"message": "Habit has been deleted!"}


@app.get("/increase_mark_counter/")
async def get_habits(habit_id: int):
    result = await AsyncORM.increase_mark_counter(habit_id=habit_id)
    return {"data": result}


@app.get("/db/")
async def db():
    await AsyncORM.create_tables()
    return "Good!"

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sql_core import AsyncORM


app = FastAPI()


@app.get("/add_user/")
async def add_user(user_id: int, **kwargs):
    await AsyncORM.add_user(user_id=user_id, **kwargs)
    return JSONResponse(
        content={"message": f"User({user_id}) created!"},
        status_code=201,
    )


@app.get("/get_habits/")
async def get_habits(user_id: int):
    habits = await AsyncORM.get_habits(user_id=user_id)
    return {"data": habits}


@app.get("/add_habit/")
async def add_habit(user_id: int):
    await AsyncORM.add_habit(user_id=user_id)
    return JSONResponse(
        content={"message": f"Habit created!"},
        status_code=201,
    )


@app.get("/edit_habit/")
async def edit_habit(user_id: int):
    # await AsyncORM.add_habit(user_id=user_id)
    return JSONResponse(
        content={"message": f"Habit editor!"},
        status_code=201,
    )


@app.get("/delete_habit/")
async def delete_habit(user_id: int):
    # await AsyncORM.add_habit(user_id=user_id)
    return JSONResponse(
        content={"message": f"Habit deleter!"},
        status_code=204,
    )


@app.get("/db/")
async def get_user_habits():
    await AsyncORM.create_tables()
    await add_user(user_id=5341671335, firstname="aa", lastname="gg", username="ffff")
    return JSONResponse(
        content={"message": "DB!"},
        status_code=201,
    )

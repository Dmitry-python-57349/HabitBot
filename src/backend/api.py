from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/get_user_habits/")
async def get_user_habits(user_id: int, limit: int):
    return JSONResponse(
        content={"message": f"User({user_id}) Habits({limit=}): []"},
        status_code=200,
    )

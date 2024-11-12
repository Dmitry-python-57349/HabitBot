from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.settings import DEBUG

app = FastAPI(debug=DEBUG)


@app.get("/")
async def index():
    return JSONResponse(
        content={"data": "Index html"},
        status_code=200,
    )

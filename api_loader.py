import uvicorn
from src.backend.api import app
from src.settings import settings


if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=settings.HOST,
        port=settings.PORT,
        log_level="info",
    )

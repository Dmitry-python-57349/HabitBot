from os import getenv
from dotenv import find_dotenv, load_dotenv

ENV_FILE = ".env"

if not find_dotenv(ENV_FILE):
    exit(f"File {ENV_FILE} not found!")

load_dotenv()


class Settings:
    BOT_TOKEN = getenv("BOT_TOKEN")
    DB_HOST = getenv("DB_HOST")
    DB_PORT = getenv("DB_PORT")
    DB_USER = getenv("DB_USER")
    DB_PASS = getenv("DB_PASS")
    DB_NAME = getenv("DB_NAME")
    HOST = getenv("HOST")
    PORT = getenv("PORT")
    PROTO = getenv("PROTO")
    MAX_MARK_COUNT = getenv("MAX_MARK_COUNT")

    @property
    def get_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()

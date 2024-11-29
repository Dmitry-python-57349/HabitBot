from os import getenv
from dotenv import find_dotenv, load_dotenv

ENV_FILE = ".env"

if not find_dotenv(ENV_FILE):
    exit(f"File {ENV_FILE} not found!")

load_dotenv()


class Settings:
    try:
        BOT_TOKEN = getenv("BOT_TOKEN")
        DB_HOST = getenv("DB_HOST")
        DB_PORT = int(getenv("DB_PORT"))
        DB_USER = getenv("DB_USER")
        DB_PASS = getenv("DB_PASS")
        DB_NAME = getenv("DB_NAME")
        HOST = getenv("HOST")
        PORT = int(getenv("PORT"))
        PROTO = getenv("PROTO")
        DEBUG = int(getenv("DEBUG"))
        MAX_MARK_COUNT = int(getenv("MAX_MARK_COUNT"))
    except ValueError:
        exit("Ошибка получения целого числа!")

    @property
    def get_db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()

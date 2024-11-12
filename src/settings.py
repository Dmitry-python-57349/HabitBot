from os import getenv
from dotenv import find_dotenv, load_dotenv

ENV_FILE = ".env"

if not find_dotenv(ENV_FILE):
    exit(f"File {ENV_FILE} not found!")

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
DEBUG = bool(getenv("DEBUG"))

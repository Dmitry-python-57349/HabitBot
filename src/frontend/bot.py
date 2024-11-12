import src.frontend.handlers as routers
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from src.settings import BOT_TOKEN

if __name__ != "__main__":
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_routers(
        routers.start_router,
    )
else:
    exit("Subfile loader.py!")

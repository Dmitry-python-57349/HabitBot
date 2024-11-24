import frontend.handlers as routers
from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from settings import settings

BOT_COMMANDS = [
    BotCommand(command=command[0], description=command[1])
    for command in [("start", "Главное меню")]
]

if __name__ != "__main__":
    bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_routers(
        routers.start_router,
        routers.habits_router,
        routers.habit_view,
        routers.habit_create,
    )

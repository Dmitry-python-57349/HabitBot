import src.frontend.handlers as routers
from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from src.settings import settings

bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

dp.include_routers(
    routers.start_router,
    routers.habits_router,
    routers.habit_view,
    routers.habit_create,
)

BOT_COMMANDS = [
    BotCommand(command=command[0], description=command[1])
    for command in [("start", "Главное меню")]
]

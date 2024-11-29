import asyncio
from asyncio.exceptions import CancelledError
from src.frontend.bot import bot, dp, BOT_COMMANDS
from src.settings import settings
from src.backend.sql_core import AsyncORM


async def main():
    if settings.DEBUG:
        await AsyncORM.create_tables()
    await bot.set_my_commands(commands=BOT_COMMANDS)
    await bot.delete_webhook(drop_pending_updates=True)
    print("БОТ запущен!")
    try:
        await dp.start_polling(bot)
    except CancelledError:
        print("БОТ остановлен!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as exc:
        exit(0)

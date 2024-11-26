import os
import asyncio
from sys import executable as python
from subprocess import Popen
from src.frontend.bot import bot, dp, BOT_COMMANDS

ABS_PATH = os.path.abspath("")


async def change_dir(app: str = ""):
    if app:
        new_path = ABS_PATH + "\\" + app
    else:
        new_path = ABS_PATH
    os.chdir(new_path)


async def main():
    try:
        await change_dir("backend")
        api_proc: Popen = Popen([python, "-m", "uvicorn", "api:app"])
        await change_dir()

        await bot.set_my_commands(commands=BOT_COMMANDS)
        await bot.delete_webhook(drop_pending_updates=True)
        try:
            await dp.start_polling(bot)
        except KeyboardInterrupt:
            api_proc.terminate()
    except Exception:
        api_proc.terminate()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        exit(0)

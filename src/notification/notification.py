from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.frontend.bot import bot
from src.backend.sql_core import AsyncORM
from src.frontend.keyboards.inline_keyboards import cleaning

scheduler = AsyncIOScheduler()
NOTIFICATION_TEXT = """
Добрый день, не забывайте о ваших ежедневных привычках 👇
"""


async def habit_notification():
    ids = await AsyncORM.user_ids()
    for elem in ids:
        await bot.send_message(
            text=NOTIFICATION_TEXT,
            chat_id=elem,
            reply_markup=cleaning,
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управляет жизненным циклом планировщика приложения.

    Args:
        app (FastAPI): Экземпляр приложения FastAPI.
    """
    try:
        # Настройка и запуск планировщика
        scheduler.add_job(
            habit_notification,
            trigger=IntervalTrigger(days=1, start_date=datetime.now()),
            id="habit_notification",
            replace_existing=True,
        )
        scheduler.start()
        print("Планировщик запущен")
        yield
    except Exception as e:
        print(f"Ошибка инициализации планировщика: {e}")
    finally:
        # Завершение работы планировщика
        scheduler.shutdown()
        print("Планировщик остановлен")

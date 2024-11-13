from aiogram import Router, F
from aiohttp import ClientSession
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from src.frontend.utils import edit_delete_bot_msg as editor
from src.frontend.states import MainStream

router = Router()


@router.callback_query(F.data == "habits_list", MainStream.Start)
async def habits_list(call: CallbackQuery, state: FSMContext):
    curr_state = await state.get_state()
    if curr_state != "MainStream:Habit_read":
        async with ClientSession() as session:
            response = await session.get(f"http://127.0.0.1:8000/get_user_habits/?user_id={call.from_user.id}&limit=20")
            text = await response.text()
            await call.answer(
                text=text,
            )
    await state.set_state(MainStream.Habit_read)


@router.callback_query(F.data == "habits_create", MainStream.Start)
async def habits_create(call: CallbackQuery, state: FSMContext):
    async with ClientSession() as session:
        response = await session.get(f"http://127.0.0.1:8000/get_user_habits/?user_id={call.from_user.id}&limit=20")
        text = await response.text()
        await call.answer(
            text=text,
        )

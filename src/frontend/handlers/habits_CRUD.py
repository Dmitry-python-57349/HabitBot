import json
from aiogram import Router, F
from aiohttp import ClientSession
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from src.frontend.states import MainStream
from src.frontend.handlers.habits_view import habit_viewer

router = Router()


@router.callback_query(F.data == "habits_list", MainStream.Start)
async def habits_list(call: CallbackQuery, state: FSMContext):
    curr_state = await state.get_state()
    if curr_state != "MainStream:Habit_read":
        async with ClientSession() as session:
            response = await session.get(f"http://127.0.0.1:8000/get_habits/?user_id={call.from_user.id}")
            content = await response.content.read()
            data = json.loads(content)
            await state.update_data(
                habits_data=data["data"],
                num_of_habits=len(data["data"]),
                curr_habit=0,
            )
        await state.set_state(MainStream.Habit_read)
    await habit_viewer(call=call, state=state)


@router.callback_query(F.data == "habits_create", MainStream.Start)
async def habits_create(call: CallbackQuery, state: FSMContext):
    async with ClientSession() as session:
        response = await session.get(f"http://127.0.0.1:8000/db/")
        text = await response.text()
        await call.answer(
            text=text,
        )

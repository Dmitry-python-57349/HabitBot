import json
from aiogram import Router, F
from aiohttp import ClientSession
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from src.frontend.states import MainStream
from src.frontend.handlers.habits_view import habit_viewer
from src.frontend.utils import edit_delete_bot_msg as editor
from src.frontend.keyboards.inline_keyboards import create_habit_markup as chm

router = Router()
CREATE_CAPTION = """
Для создания привычки необходимо добавить название и описание!
——————————————————————
Текущее название: {habit_name}

Текущее описание: {habit_desc}
——————————————————————

Кликай на кнопки ниже чтобы добавить их 👇
"""
ABSENT_WORD = "не указано"


@router.callback_query(F.data == "habits_list", MainStream.Start)
async def habits_list(call: CallbackQuery, state: FSMContext):
    curr_state = await state.get_state()
    if curr_state != "MainStream:Habit_read":
        async with ClientSession() as session:
            response = await session.get(
                f"http://127.0.0.1:8000/get_habits/?user_id={call.from_user.id}"
            )
            content = await response.content.read()
            data = json.loads(content)
            await state.update_data(
                habits_data=data["data"],
                num_of_habits=len(data["data"]),
            )
        await state.set_state(MainStream.Habit_read)
    await habit_viewer(call=call, state=state)


@router.callback_query(F.data == "habits_create", MainStream.Start)
async def habits_create(
    call: CallbackQuery | None = None, state: FSMContext | None = None
):
    state_data = await state.get_data()
    name, desc = state_data["habit_name"], state_data["habit_desc"]
    await editor(
        msg=state_data["bot_msg"],
        caption=CREATE_CAPTION.format(
            habit_name=name if name else ABSENT_WORD,
            habit_desc=desc if desc else ABSENT_WORD,
        ),
        markup=chm,
    )
    await state.set_state(MainStream.Habit_create)

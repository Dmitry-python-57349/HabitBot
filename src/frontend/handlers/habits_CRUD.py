import json
from aiogram import Router, F
from aiohttp import ClientSession
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from src.frontend.states import MainStream
from src.frontend.handlers.habits_view import habit_viewer
from src.frontend.utils import (
    edit_delete_bot_msg as editor,
    delete_fixer,
    get_url,
    increase_mark_counter,
    delete_habit_by_id,
)
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
async def habits_list(
    call: CallbackQuery | Message | None = None, state: FSMContext | None = None
):
    curr_state = await state.get_state()
    if curr_state != "MainStream:Habit_read":
        async with ClientSession() as session:
            params = {"user_id": call.from_user.id}
            url = await get_url(url_path="get_habits", params=params)
            response = await session.get(url=url)
            content = await response.content.read()
            data = json.loads(content)
            await state.update_data(
                habits_data=data["data"],
                num_of_habits=len(data["data"]),
            )
            await delete_fixer(state=state)
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


@router.callback_query(F.data == "habit_delete", MainStream.Habit_read)
async def habit_delete(
    call: CallbackQuery | None = None, state: FSMContext | None = None
):
    state_data = await state.get_data()
    habits_data, curr_habit = state_data["habits_data"], state_data["curr_habit"]
    habit_id = habits_data[curr_habit]["id"]
    await delete_habit_by_id(habit_id=habit_id)
    await call.answer(text="Привычка удалена!")
    await state.set_state(MainStream.Habit_delete)
    await habits_list(call=call, state=state)


@router.callback_query(F.data == "habit_mark", MainStream.Habit_read)
async def habit_mark(
    call: CallbackQuery | None = None, state: FSMContext | None = None
):
    state_data = await state.get_data()
    curr_habit, habits_data = (
        state_data["curr_habit"],
        state_data["habits_data"],
    )
    habit_id = habits_data[curr_habit]["id"]
    status = habits_data[curr_habit]["today_mark"]

    if status:
        await call.answer(text="Вы уже отметили данную привычку!")
        return

    res = await increase_mark_counter(habit_id=habit_id)
    if not res:
        await delete_habit_by_id(habit_id=habit_id)
        await call.answer(text="Вы смогли привить новую привычку! Поздравляем 🎉")
        await habit_viewer(state=state)
        return

    habits_data[curr_habit]["today_mark"] = True
    await state.update_data(habits_data=habits_data)
    await call.answer(text="Привычка отмечена!")
    await habit_viewer(state=state)

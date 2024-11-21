from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from src.frontend.utils import edit_delete_bot_msg as editor
from src.frontend.states import MainStream
from src.frontend.keyboards.inline_keyboards import (
    habit_markup_builder,
    habit_index_error_markup as habit_error_m,
)

router = Router()
HABIT_CAPTION = """
Привычка #{curr_habit}
——————————————————————            
Название: {name}

Описание: {description}
"""
HABIT_INDEX_ERROR = """
На данный момент у вас не добавлено ни одной привычки.

Нажми на кнопку "добавить привычку" чтобы исправить это 👇
"""


@router.callback_query(F.data.in_(["next", "prev"]), MainStream.Habit_read)
async def next_prev(call: CallbackQuery | None = None, state: FSMContext | None = None):
    state_data = await state.get_data()
    curr_habit, num_of_habits = state_data["curr_habit"], state_data["num_of_habits"]
    if num_of_habits == 1:
        await call.answer(text="У тебя одна привычка, куда листаешь?)")
        return
    list_num_of_habits = num_of_habits - 1
    match call.data:
        case "next":
            if curr_habit < list_num_of_habits:
                curr_habit += 1
                await state.update_data(curr_habit=curr_habit)
            else:
                await state.update_data(curr_habit=0)

            await habit_viewer(call=call, state=state)
        case "prev":
            if curr_habit > 0:
                curr_habit -= 1
                await state.update_data(curr_habit=curr_habit)
            else:
                await state.update_data(curr_habit=list_num_of_habits)

            await habit_viewer(call=call, state=state)
        case _:
            ...


@router.callback_query(F.data == "habit_viewer", MainStream.Habit_read)
async def habit_viewer(
    call: CallbackQuery | None = None, state: FSMContext | None = None
):
    state_data = await state.get_data()
    curr_habit, num_of_habits, habits_data = (
        state_data["curr_habit"],
        state_data["num_of_habits"],
        state_data["habits_data"],
    )

    habit_markup = await habit_markup_builder(
        curr_habit=curr_habit + 1,
        num_of_habits=num_of_habits,
    )
    try:
        name = habits_data[curr_habit]["name"]
        description = habits_data[curr_habit]["description"]
    except IndexError:
        await editor(
            msg=state_data["bot_msg"],
            caption=HABIT_INDEX_ERROR,
            markup=habit_error_m,
        )
        await state.set_state(MainStream.Start)
        return
    await editor(
        msg=state_data["bot_msg"],
        caption=HABIT_CAPTION.format(
            curr_habit=curr_habit + 1,
            name=name,
            description=description,
        ),
        markup=habit_markup,
    )


@router.callback_query(F.data == "page_num", MainStream.Habit_read)
async def blank(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    curr_habit, num_of_habits = state_data["curr_habit"], state_data["num_of_habits"]
    curr_habit += 1
    await call.answer(text=f"<{curr_habit} из {num_of_habits}>")

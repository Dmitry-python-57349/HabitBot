from aiogram import Router, F
from aiohttp import ClientSession
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from src.frontend.states import MainStream
from src.frontend.utils import edit_delete_bot_msg as editor, edit_habit
from src.frontend.handlers.habits_CRUD import habits_create, habits_list
from src.frontend.filters import ListStateFilter

router = Router()


@router.callback_query(
    F.data.startswith("habit_create_") | F.data.startswith("habit_edit_"),
    ListStateFilter([MainStream.Habit_create, MainStream.Habit_read]),
)
async def habits_handler(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    next_move = call.data.split("_")
    match next_move[1], next_move[2]:
        case "create", "name":
            await editor(
                msg=state_data["bot_msg"],
                caption="Отправьте название привычки:",
            )
            await state.set_state(MainStream.Habit_create_name)
        case "create", "description":
            await editor(
                msg=state_data["bot_msg"],
                caption="Отправьте описание привычки:",
            )
            await state.set_state(MainStream.Habit_create_desc)
        case "edit", "name":
            await editor(
                msg=state_data["bot_msg"],
                caption="Отправьте новое название привычки:",
            )
            await state.set_state(MainStream.Habit_edit_name)
        case "edit", "desc":
            await editor(
                msg=state_data["bot_msg"],
                caption="Отправьте новое описание привычки:",
            )
            await state.set_state(MainStream.Habit_edit_desc)


@router.message(
    ListStateFilter(
        [
            MainStream.Habit_create_name,
            MainStream.Habit_create_desc,
            MainStream.Habit_edit_name,
            MainStream.Habit_edit_desc,
        ]
    )
)
async def msg_handler(message: Message, state: FSMContext):
    state_name = await state.get_state()
    next_move = state_name.split("_")
    match next_move[1], next_move[2]:
        case "create", "name":
            await state.update_data(habit_name=message.text)
        case "create", "desc":
            await state.update_data(habit_desc=message.text)
        case "edit", "name":
            await editor(msg=message)
            await edit_habit(state=state, name=message.text)
            await state.set_state(MainStream.Start)
            await habits_list(call=message, state=state)
            return
        case "edit", "desc":
            await editor(msg=message)
            await edit_habit(state=state, description=message.text)
            await state.set_state(MainStream.Start)
            await habits_list(call=message, state=state)
            return
    await editor(msg=message)
    await habits_create(state=state)


@router.callback_query(F.data == "habit_save", MainStream.Habit_create)
async def habits_save(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    name, desc = state_data["habit_name"], state_data["habit_desc"]
    if not all([name and desc]):
        await call.answer(text="Недостаточно данных для создания привычки!")
        return
    async with ClientSession() as session:
        data = {
            "user_id": call.from_user.id,
            "name": name,
            "description": desc,
        }
        await session.post("http://127.0.0.1:8000/add_habit/", json=data)
    await call.answer(text="Привычка создана!")
    await state.update_data(
        habit_name="",
        habit_desc="",
    )

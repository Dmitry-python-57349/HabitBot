from aiogram import Router, F
from aiohttp import ClientSession
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from src.frontend.states import MainStream
from src.frontend.utils import edit_delete_bot_msg as editor
from src.frontend.handlers.habits_CRUD import habits_create
from src.frontend.filters import ListStateFilter

router = Router()


@router.callback_query(F.data.startswith("habit_create_"), MainStream.Habit_create)
async def habits_handler(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    next_move = call.data.split("_")[2]
    match next_move:
        case "name":
            await editor(
                msg=state_data["bot_msg"],
                caption="Отправьте название привычки:",
            )
            await state.set_state(MainStream.Habit_create_name)
        case "description":
            await editor(
                msg=state_data["bot_msg"],
                caption="Отправьте описание привычки:",
            )
            await state.set_state(MainStream.Habit_create_desc)


@router.message(
    ListStateFilter(states=[MainStream.Habit_create_name, MainStream.Habit_create_desc])
)
async def msg_handler(message: Message, state: FSMContext):
    state_name = await state.get_state()
    next_move = state_name.split("_")[2]
    match next_move:
        case "name":
            await state.update_data(habit_name=message.text)
        case "desc":
            await state.update_data(habit_desc=message.text)
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

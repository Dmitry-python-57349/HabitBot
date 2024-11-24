from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, InputMediaPhoto, CallbackQuery
from frontend.utils import (
    edit_delete_bot_msg as editor,
    get_success_image_path as get_path,
    reg_user,
)
from frontend.states import MainStream
from frontend.keyboards.inline_keyboards import reg_markup as reg, start_markup

router = Router()


@router.message(Command(commands=["start"]))
async def first_start(msg: Message, state: FSMContext):
    curr_state = await state.get_state()
    await editor(msg=msg)

    if curr_state is not None:
        return await home(state=state)

    await state.set_state(MainStream.Start)
    photo = FSInputFile(get_path(name="start.webp"))

    bot_msg = await msg.bot.send_photo(
        chat_id=msg.chat.id,
        photo=photo,
        caption="Для начала работы необходимо зарегистрироваться, нажми кнопку ниже! 👇",
        reply_markup=reg,
    )
    await state.update_data(
        bot_msg=bot_msg,
        start_photo=InputMediaPhoto(media=photo),
        curr_habit=0,
        habit_name="",
        habit_desc="",
    )
    await reg_user(user=msg.from_user)


@router.callback_query(F.data == "home")
async def home(call: CallbackQuery | None = None, state: FSMContext | None = None):
    curr_state = await state.get_state()

    if curr_state != "MainStream:Start":
        await state.set_state(MainStream.Start)

    state_data = await state.get_data()
    await editor(
        msg=state_data["bot_msg"],
        caption="⭐ Главное меню ⭐",
        markup=start_markup,
    )


@router.callback_query(F.data == "clean")
async def clean(call: CallbackQuery, state: FSMContext):
    await editor(call.message)
    await call.answer(text="Очищено!")

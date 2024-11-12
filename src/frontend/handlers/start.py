from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, InputMediaPhoto, CallbackQuery
from src.frontend.utils import edit_delete_bot_msg as editor, get_success_image_path as get_path
from src.frontend.states import MainStream
from src.frontend.keyboards.inline_keyboards import reg_markup as reg, start_markup

router = Router()


@router.message(Command(commands=["start"]))
async def msg_start(msg: Message, state: FSMContext):
    curr_state = await state.get_state()
    if curr_state is not None:
        return
    await state.set_state(MainStream.Start)
    await editor(entity=msg)
    photo = FSInputFile(get_path(name="start.webp"))
    bot_msg = await msg.bot.send_photo(
        chat_id=msg.chat.id,
        photo=photo,
        caption="Для начала работы необходимо зарегистрироваться, нажми кнопку ниже! 👇",
        reply_markup=reg,
    )
    await state.update_data(bot_msg=bot_msg, start_photo=InputMediaPhoto(media=photo))


@router.callback_query(F.data == "start", MainStream.Start)
async def call_start(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    await editor(
        entity=call,
        caption="⭐ Главное меню ⭐",
        picture=state_data["start_photo"],
        markup=start_markup,
    )

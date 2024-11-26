import os.path
from aiohttp import ClientSession
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto, InlineKeyboardMarkup
from aiogram.types.user import User as TgUser
from src.settings import settings

ABS_PATH = os.path.abspath("src")


async def edit_delete_bot_msg(
    msg: Message,
    caption: str | None = None,
    picture: InputMediaPhoto | None = None,
    markup: InlineKeyboardMarkup | None = None,
) -> None:

    if isinstance(msg, Message):
        chat_id = msg.chat.id
        message_id = msg.message_id
        bot = msg.bot
    else:
        raise Exception("bot_msg not Message instance!")

    if picture:
        await bot.edit_message_media(
            media=picture,
            chat_id=chat_id,
            message_id=message_id,
        )

    if caption:
        if markup:
            await bot.edit_message_caption(
                caption=caption,
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=markup,
            )
            return
        await bot.edit_message_caption(
            caption=caption,
            chat_id=chat_id,
            message_id=message_id,
        )
        return

    await bot.delete_message(
        chat_id=chat_id,
        message_id=message_id,
    )


async def delete_fixer(state: FSMContext) -> None:
    state_ = await state.get_state()
    state_data = await state.get_data()
    num_of_habits, curr_habit = state_data["num_of_habits"], state_data["curr_habit"]
    list_num = num_of_habits - 1
    if state_ == "MainStream:Habit_delete":
        if 0 < curr_habit < list_num:
            return
        if curr_habit > list_num:
            await state.update_data(curr_habit=list_num)


async def edit_habit(state: FSMContext, **kwargs) -> None:
    state_data = await state.get_data()
    habits_data, curr_habit = state_data["habits_data"], state_data["curr_habit"]
    json_data = {"habit_id": habits_data[curr_habit]["id"]}
    json_data.update(**kwargs)
    async with ClientSession() as session:
        url = await get_url(url_path="edit_habit")
        await session.put(
            url=url,
            json=json_data,
        )


async def get_url(url_path: str = "", params: dict | None = None) -> str:
    result = f"{settings.PROTO}://{settings.HOST}:{settings.PORT}/"
    if url_path:
        result += f"{url_path}/"
    if params:
        result += "?" + "&".join([f"{k}={v}" for k, v in params.items()])
    return result


async def reg_user(user: TgUser) -> None:
    user_data = {
        "user_id": user.id,
        "username": user.username,
        "firstname": user.first_name,
        "lastname": user.last_name,
    }
    async with ClientSession() as session:
        url = await get_url(url_path="add_user")
        await session.post(url=url, json=user_data)


def get_success_image_path(name: str) -> str:
    return ABS_PATH + f"\\frontend\\images\\{name}"

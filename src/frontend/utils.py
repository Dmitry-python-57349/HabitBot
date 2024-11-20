import os.path
from aiogram.types import Message, InputMediaPhoto, InlineKeyboardMarkup

ABS_PATH = os.path.abspath("")


async def edit_delete_bot_msg(
        msg: Message,
        caption: str | None = None,
        picture: InputMediaPhoto | None = None,
        markup: InlineKeyboardMarkup | None = None
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


def get_success_image_path(name: str) -> str:
    return ABS_PATH + f"\\frontend\\images\\{name}"

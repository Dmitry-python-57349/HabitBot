import os.path
from aiogram.types import Message, InputMediaPhoto, CallbackQuery, InlineKeyboardMarkup

ABS_PATH = os.path.abspath("")


async def edit_delete_bot_msg(
        entity: Message | CallbackQuery,
        caption: str | None = None,
        picture: InputMediaPhoto | None = None,
        markup: InlineKeyboardMarkup | None = None
) -> None:

    if isinstance(entity, Message):
        chat_id = entity.chat.id
        message_id = entity.message_id
    else:
        chat_id = entity.message.chat.id
        message_id = entity.message.message_id

    if picture:
        await entity.bot.edit_message_media(
            media=picture,
            chat_id=chat_id,
            message_id=message_id,
        )

    if caption:
        if markup:
            await entity.bot.edit_message_caption(
                caption=caption,
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=markup,
            )
            return
        await entity.bot.edit_message_caption(
            caption=caption,
            chat_id=chat_id,
            message_id=message_id,
        )
        return

    await entity.bot.delete_message(
        chat_id=chat_id,
        message_id=message_id,
    )


def get_success_image_path(name: str) -> str:
    return ABS_PATH + f"\\frontend\\images\\{name}"

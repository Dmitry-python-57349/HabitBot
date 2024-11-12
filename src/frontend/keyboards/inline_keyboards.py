from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

reg_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Зарегистрироваться 📝", callback_data="start")
        ]
    ]
)

start_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="First 📝", callback_data="first")
        ],
        [
            InlineKeyboardButton(text="Second 📝", callback_data="second")
        ]
    ]
)

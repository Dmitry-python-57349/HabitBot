from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

reg_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Зарегистрироваться 📝", callback_data="home")
        ]
    ]
)

start_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Список привычек 📑", callback_data="habits_list")
        ],
        [
            InlineKeyboardButton(text="Добавить привычку ✏", callback_data="habits_create")
        ]
    ]
)

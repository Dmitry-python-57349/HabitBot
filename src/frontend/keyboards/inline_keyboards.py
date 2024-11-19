from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

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


async def habit_markup_builder(
        curr_habit: int | str,
        num_of_habits: int | str,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Редактировать 📝", callback_data="habit_edit"),
        InlineKeyboardButton(text="Удалить 🗑", callback_data="habit_delete"),
        InlineKeyboardButton(text="←", callback_data="prev"),
        InlineKeyboardButton(text=f"{curr_habit} / {num_of_habits}", callback_data="page_num"),
        InlineKeyboardButton(text="→", callback_data="next"),
        InlineKeyboardButton(text="Главное меню 🏡", callback_data="home")
    )
    builder.adjust(1, 1, 3, 1)
    return builder.as_markup()

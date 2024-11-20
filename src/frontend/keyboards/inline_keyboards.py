from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

reg_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Зарегистрироваться 📝", callback_data="home")]
    ]
)

start_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Список привычек 📑", callback_data="habits_list")],
        [
            InlineKeyboardButton(
                text="Добавить привычку ✏", callback_data="habits_create"
            )
        ],
    ]
)

create_habit_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Добавить название", callback_data="habit_create_name"
            ),
            InlineKeyboardButton(
                text="Добавить описание", callback_data="habit_create_description"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Сохранить привычку 💾", callback_data="habit_save"
            ),
        ],
        [
            InlineKeyboardButton(text="Главное меню 🏡", callback_data="home"),
        ],
    ]
)


async def habit_markup_builder(
    curr_habit: int | str,
    num_of_habits: int | str,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Изменить название", callback_data="habit_edit"),
        InlineKeyboardButton(text="Изменить описание", callback_data="habit_edit"),
        InlineKeyboardButton(text="Удалить 🗑", callback_data="habit_delete"),
        InlineKeyboardButton(text="←", callback_data="prev"),
        InlineKeyboardButton(
            text=f"{curr_habit} / {num_of_habits}", callback_data="page_num"
        ),
        InlineKeyboardButton(text="→", callback_data="next"),
        InlineKeyboardButton(text="Главное меню 🏡", callback_data="home"),
    )
    builder.adjust(2, 1, 3, 1)
    return builder.as_markup()

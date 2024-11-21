from aiogram.fsm.state import State, StatesGroup


class MainStream(StatesGroup):
    Start = State()
    Habit_create = State()
    Habit_create_name = State()
    Habit_create_desc = State()
    Habit_read = State()
    Habit_edit_name = State()
    Habit_edit_desc = State()
    Habit_delete = State()

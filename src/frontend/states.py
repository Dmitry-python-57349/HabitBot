from aiogram.fsm.state import State, StatesGroup


class MainStream(StatesGroup):
    Start = State()
    Habit_create = State()
    Habit_read = State()
    Habit_update = State()
    Habit_delete = State()

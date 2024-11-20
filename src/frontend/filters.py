from typing import Sequence

from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import Message


class ListStateFilter(Filter):
    """Фильтр на группу состояний"""

    def __init__(self, states: Sequence[State]):
        self.states = states

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        curr_state = await state.get_state()
        return curr_state in self.states

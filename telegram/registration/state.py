from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    name = State()
    phone = State()

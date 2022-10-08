from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
    choose_address = State()

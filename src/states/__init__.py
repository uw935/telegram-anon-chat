from aiogram.fsm.state import StatesGroup, State


class Chat(StatesGroup):
    menu = State()
    private_chat = State()
    awaiting_chat = State()

from aiogram.fsm.state import StatesGroup, State


class Menu(StatesGroup):
    general: State = State()

class Chat(StatesGroup):
    private_chat: State = State()
    loading_chat: State = State()

from aiogram.fsm.state import StatesGroup, State


class Chat(StatesGroup):
    private_chat: State = State()
    loading_chat: State = State()

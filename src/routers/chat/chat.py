from states import Chat
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config import TEXTS, AVAILABLE_TYPES


router = Router()


async def get_user_chat(*, state: FSMContext) -> int:
    _result = await state.get_data()
    _result = _result.get("CURRENT_CHAT")

    if _result is None:
        return

    return int(_result)


@router.message(Chat.private_chat)
async def private_chat_handler(message: Message, state: FSMContext) -> None:
    current_chat_id = await get_user_chat(state=state)

    if message.content_type not in AVAILABLE_TYPES:
        await message.reply(TEXTS["states"]["menu"]["chat_type_error"])
        return

    await message.send_copy(current_chat_id)


@router.message(Chat.loading_chat)
async def loading_chat_handler(message: Message) -> None:
    await message.reply(TEXTS["states"]["menu"]["loading_wait"])

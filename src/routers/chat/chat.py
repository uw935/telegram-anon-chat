from states import Chat
from loguru import logger
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


router = Router()


@router.message(Chat.private_chat)
async def private_chat_handler(message: Message, bot: Bot, state: FSMContext) -> None:
    current_chat_id = await state.get_data()
    logger.debug(current_chat_id)
    current_chat_id = current_chat_id.get("CURRENT_CHAT")

    logger.debug(current_chat_id)

    await bot.send_message(current_chat_id, message.text)


# make private chat photo handler

from config import bot
from states import Chat
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


router = Router()


@router.message(Chat.private_chat)
async def private_chat_handler(message: Message, state: FSMContext) -> None:
    current_chat_id = await state.get_data().get("CURRENT_CHAT")
    
    await bot.send_message(current_chat_id, message.text)

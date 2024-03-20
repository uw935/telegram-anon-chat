from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import Chat
from config import TEXTS
from methods.chat import get_user_chat, is_valide_message


router = Router()


@router.message(Chat.private_chat)
async def private_chat_handler(message: Message, state: FSMContext) -> None:
    '''
    Handler to all the messages in private_chat mode.
    Working only in the private_chat mode.
    Private mode is when the user is in the chat with somewho right now.

    :param message: Telergam Message
    :param state: State of the user
    '''

    current_chat_id = await get_user_chat(state=state)
    validate_message = await is_valide_message(
        message=message.text,
        message_type=message.content_type
    )

    if validate_message:
        await message.send_copy(current_chat_id)
        return
    
    await message.reply(TEXTS["states"]["chat"]["type_error"])


@router.message(Chat.loading_chat)
async def loading_chat_handler(message: Message) -> None:
    '''
    Handler to all the messages in loading_chat mode.
    Working only in the loading_chat mode.
    Loading chat mode is when the user is waiting new chat to be started.

    :param message: Telergam Message
    '''

    await message.reply(text=TEXTS["states"]["chat"]["still_searching"])

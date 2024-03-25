from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config import TEXTS
from models.states import Chat
from methods.user import User
from methods.messages import Message as MethodMessage


router = Router()


@router.message(Chat.private_chat)
async def private_chat_handler(message: Message, state: FSMContext) -> None:
    """
    Handler to all the messages in private_chat mode.
    Working only in the private_chat mode.
    Private mode is when the user is in the chat with somewho right now.

    :param message: Telergam Message
    :param state: State of the user
    """

    chat = await User(
        user_id=str(message.from_user.id),
        state=state
    ).get_chat()

    validate_message = await MethodMessage.is_valid_message(
        message=message.text or message.caption,
        message_type=message.content_type
    )

    if validate_message:
        await message.send_copy(
            chat_id=chat.companion.user_id,
        )

        return

    await message.reply(text=TEXTS["states"]["chat"]["type_error"])


@router.message(Chat.loading_chat)
async def loading_chat_handler(message: Message) -> None:
    """
    Handler to all the messages in loading_chat mode.
    Working only in the loading_chat mode.
    Loading chat mode is when the user is waiting new chat to be started.

    :param message: Telergam Message
    """

    await message.reply(text=TEXTS["states"]["chat"]["still_searching"])

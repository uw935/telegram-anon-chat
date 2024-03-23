from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram import Router, F, Bot, Dispatcher
from aiogram.types import Message, CallbackQuery

from models.states import Chat
from methods.user import User
from config import TEXTS
from keyboard import MAIN_MENU


router = Router()


@router.message(Command("newchat"))
async def command_new_chat_handler(
    message: Message,
    dispatcher: Dispatcher,
    bot: Bot,
    state: FSMContext
) -> None:
    '''
    Handler to the "/newchat" command

    :param message: Telergam Message
    :param dispatcher: Instance of the current dispatcher
    :param bot: Instance of the current bot
    :param state: State of the user
    '''

    await User(
        user_id=str(message.from_user.id),
        dispatcher=dispatcher,
        bot=bot,
        state=state
    ).start_new_chat()


@router.message(Chat.private_chat, Command("stopchat"))
async def command_stop_chat_handler(
    message: Message,
    dispatcher: Dispatcher,
    bot: Bot,
    state: FSMContext
) -> None:
    '''
    Handler to the "/stop" command.
    Working only in the private_chat mode.
    Private mode is when the user is in the chat with somewho right now.

    :param message: Telergam Message
    :param dispatcher: Instance of the current dispatcher
    :param bot: Instance of the current bot
    :param state: State of the user
    '''

    user = User(
        user_id=str(message.from_user.id),
        bot=bot,
        dispatcher=dispatcher,
        state=state
    )

    await user.stop_chat()

    await bot.send_message(
        chat_id=user.user_id,
        text=TEXTS["states"]["menu"]["general"],
        reply_markup=MAIN_MENU
    )


@router.callback_query(Chat.private_chat, F.data == "STOP_THIS_CHAT")
async def callback_stop_chat_handler(
    callback: CallbackQuery,
    dispatcher: Dispatcher,
    bot: Bot,
    state: FSMContext
) -> None:
    '''
    Handler to the "STOP_THIS_CHAT" callback.
    This callback triggers when user hit the "Stop chat" button.
    Working only in the private_chat mode.
    Private mode is when the user is in the chat with somewho right now.

    :param callback: Telergam CallbackQuery
    :param dispatcher: Instance of the current dispatcher
    :param bot: Instance of the current bot
    :param state: State of the user
    '''

    user = User(
        user_id=str(callback.from_user.id),
        bot=bot,
        dispatcher=dispatcher,
        state=state
    )

    await user.stop_chat()
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=TEXTS["states"]["menu"]["general"],
        reply_markup=MAIN_MENU,
    )


@router.callback_query(Chat.loading_chat, F.data == "STOP_SEARCH")
async def callback_stop_search_handler(
    callback: CallbackQuery,
    bot: Bot,
    state: FSMContext
) -> None:
    '''
    Handler to the "STOP_SEARCH" callback.
    This callback triggers when user hit the "Stop search" button.
    Working only in the loading_chat mode.
    Loading chat mode is when the user is waiting new chat to be started.

    :param callback: Telergam CallbackQuery
    :param bot: Instance of the current bot
    :param state: State of the user
    '''

    user = User(
        user_id=str(callback.from_user.id),
        state=state,
        bot=bot
    )

    await user.clear()

    await bot.send_message(
        chat_id=user.user_id,
        text=TEXTS["states"]["chat"]["stop_search"]
    )

    await bot.send_message(
        chat_id=user.user_id,
        text=TEXTS["states"]["menu"]["general"],
        reply_markup=MAIN_MENU,
    )


@router.callback_query(F.data == "START_NEW_CHAT")
async def callback_new_chat_handler(
    callback: CallbackQuery,
    dispatcher: Dispatcher,
    bot: Bot,
    state: FSMContext
) -> None:
    '''
    Handler to the "START_NEW_CHAT" callback.
    This callback triggers when user hit the "Start new chat" button.

    :param callback: Telergam CallbackQuery
    :param dispatcher: Instance of the current dispatcher
    :param bot: Instance of the current bot
    :param state: State of the user
    '''

    await User(
        user_id=str(callback.from_user.id),
        dispatcher=dispatcher,
        bot=bot,
        state=state
    ).start_new_chat()

@router.message(default_state)
async def message_handler(message: Message) -> None:
    '''
    Handler to all messages.

    :param message: Telergam Message
    '''

    await message.answer(
        text=TEXTS["states"]["menu"]["general"],
        reply_markup=MAIN_MENU
    )

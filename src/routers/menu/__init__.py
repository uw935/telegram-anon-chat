import random

from loguru import logger
from aiogram import Router, F, Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from states import Chat
from config import TEXTS
from routers.menu.keyboard import MAIN_MENU


router = Router()
users_searching = []


async def stop_this_chat(*, user_id: str, bot: Bot, dispatcher: Dispatcher, state: FSMContext) -> None:
    if user_id not in users_searching:
        users_searching.append(user_id)

    current_chat_id = await state.get_data()
    current_chat_id = current_chat_id.get("CURRENT_CHAT")

    if current_chat_id is None:
        return
    
    current_chat_id = int(current_chat_id)
    companion_state = dispatcher.fsm.resolve_context(bot, current_chat_id, current_chat_id)

    await companion_state.clear()
    await state.clear()

    await bot.send_message(
        current_chat_id, TEXTS["states"]["menu"]["chat_ended_companion"]
    )
    await bot.send_message(user_id, TEXTS["states"]["menu"]["chat_ended"])


async def start_new_chat(*, user_id: str, bot: Bot, dispatcher: Dispatcher, state: FSMContext) -> None:
    await stop_this_chat(user_id=user_id, bot=bot, dispatcher=dispatcher,  state=state)
    random_user = random.choice(users_searching)

    if random_user is not None and random_user != user_id:
        del users_searching[users_searching.index(user_id)]
        del users_searching[users_searching.index(random_user)]
        
        random_user = int(random_user)

        companion_state = dispatcher.fsm.resolve_context(bot, random_user, random_user)

        await companion_state.set_data({"CURRENT_CHAT": user_id})
        await companion_state.set_state(Chat.private_chat)
        
        await state.set_data({"CURRENT_CHAT": random_user})
        await state.set_state(Chat.private_chat)

        await bot.send_message(random_user, TEXTS["states"]["menu"]["chat_found"])
        await bot.send_message(user_id, TEXTS["states"]["menu"]["chat_found"])

        return

    # looking for awaiting other users
    await bot.send_message(user_id, "Nobody found")


@router.message(Command("newchat"))
async def command_new_chat_handler(message: Message, dispatcher: Dispatcher, bot: Bot, state: FSMContext) -> None:
    await start_new_chat(user_id=str(message.from_user.id), dispatcher=dispatcher, bot=bot, state=state)


@router.callback_query(F.data == "START_NEW_CHAT")
async def callback_new_chat_handler(callback: CallbackQuery, dispatcher: Dispatcher, bot: Bot, state: FSMContext) -> None:
    await start_new_chat(user_id=str(callback.from_user.id), dispatcher=dispatcher, bot=bot, state=state)


@router.message(default_state)
async def menu(message: Message, state: FSMContext) -> None:
    if (user_id := str(message.chat.id)) not in users_searching:
        users_searching.append(user_id)

    await message.answer(TEXTS["states"]["menu"]["general"], reply_markup=MAIN_MENU)

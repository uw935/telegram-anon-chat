import random

from config import bot
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states import Chat, Menu
from config import TEXTS
from routers.menu.keyboard import MAIN_MENU


router = Router()
users_not_in_chat = []


async def stop_this_chat(*, user_id: str, state: FSMContext) -> None:
    if user_id not in users_not_in_chat:
        users_not_in_chat.append(user_id)

    current_chat_id = await state.get_data()
    current_chat_id = current_chat_id.get("CURRENT_CHAT")

    if current_chat_id is None:
        return

    await state.set_state(Menu.general)

    await bot.send_message(current_chat_id, TEXTS["states"]["menu"]["chat_ended_companion"])
    await bot.send_message(user_id, TEXTS["states"]["menu"]["chat_ended"])


async def start_new_chat(*, user_id: str, state: FSMContext) -> None:
    await stop_this_chat(user_id=user_id, state=state)
    random_user = random.choice(users_not_in_chat)

    if random_user is not None and random_user != user_id:
        del users_not_in_chat[users_not_in_chat.index(user_id)]
        del users_not_in_chat[users_not_in_chat.index(random_user)]

        await state.set_data(
            {
                "CURRENT_CHAT": random_user
            }
        )

        await state.set_state(Chat.private_chat)
        await bot.send_message(user_id, TEXTS["states"]["menu"]["chat_found"])

        return

    # looking for awaiting other users
    await bot.send_message(user_id, "Nobody found")


@router.message(Command("newchat"))
async def command_new_chat_handler(message: Message, state: FSMContext) -> None:
    await start_new_chat(user_id=str(message.from_user.id), state=state)


@router.callback_query(F.data == "START_NEW_CHAT")
async def callback_new_chat_handler(callback: CallbackQuery, state: FSMContext) -> None:
    print(users_not_in_chat)
    await start_new_chat(user_id=str(callback.from_user.id), state=state)


@router.message()
async def menu(message: Message) -> None:
    if (user_id := str(message.chat.id)) not in users_not_in_chat:
        users_not_in_chat.append(user_id)

    await message.answer(TEXTS["states"]["menu"]["general"], reply_markup=MAIN_MENU)

import random
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext

from states import Chat
from config import TEXTS
from keyboard import MAIN_MENU, STOP_WAIT


users_searching = []


async def get_user_chat(*, state: FSMContext) -> int:
    '''
    Get user_id of the companion (user, that state_user in chat with)

    :param state: State of the user you want to get chat from.
    :return: Integer, ID of the companion
    if user have current chat and None otherwise.
    '''

    _result = await state.get_data()
    _result = _result.get("CURRENT_CHAT")

    if _result is None:
        return

    return int(_result)


async def clear_user(*, state: FSMContext, user_id: str):
    '''
    Clearing user chat information and state too

    :param state: State of the user we want to clean.
    :param user_id: User ID
    '''

    if user_id in users_searching:
        del users_searching[users_searching.index(user_id)]

    await state.clear()


async def stop_this_chat(
    *,
    user_id: str,
    bot: Bot,
    dispatcher: Dispatcher,
    state: FSMContext
) -> None:
    '''
    Stoping current chat by user ID

    :param user_id: ID of the user whose chat we want to stop.
    :param bot: Instance of current bot.
    :param dispatcher: Instance of current dispatcher.
    :param state: State of the user whose chat we want to stop.
    '''

    companion_chat_id = await get_user_chat(state=state)

    # If there is no company with this user
    # Don't stop the chat.
    if companion_chat_id is None:
        return

    # If user have company, clearing data of our companion
    # Also getting his state by resolve_context
    await clear_user(
        state=dispatcher.fsm.resolve_context(
            bot=bot,
            chat_id=companion_chat_id,
            user_id=companion_chat_id
        ),
        user_id=companion_chat_id
    )

    # And ours too.
    await clear_user(
        state=state,
        user_id=user_id
    )

    # Sending that chat is over
    await bot.send_message(
        chat_id=companion_chat_id,
        text=TEXTS["states"]["chat"]["finish_by_companion"]
    )

    # So this user is in menu now
    # Sending menu messages to our companion.
    await bot.send_message(
        chat_id=companion_chat_id,
        text=TEXTS["states"]["menu"]["general"],
        reply_markup=MAIN_MENU
    )

    await bot.send_message(
        chat_id=user_id,
        text=TEXTS["states"]["chat"]["finish"]
    )


async def wait_new_chat(user_id: str, bot: Bot, state: FSMContext) -> None:
    '''
    Make user wait his new chat by user ID

    :param user_id: ID of user, that we want to be waiting
    :param bot: Bot instance
    :param state: State of the user
    '''

    await add_user_in_search(user_id=user_id)
    await state.set_state(state=Chat.loading_chat)
    await bot.send_message(
        chat_id=user_id,
        text=TEXTS["states"]["chat"]["search"]
    )

    iteration = 0

    # Checking if in users, who searcing for new contacts,
    # ..only one user, so this is means that we alone here.
    while True:
        await asyncio.sleep(0.1)
        iteration += 1

        chat_not_found = await state.get_state()
        
        if chat_not_found == Chat.private_chat:
            break
        
        # On the 3th seconds printing out wait_too_long message.
        # 30 = 3 * 10 => because we divided 1 sec to 0.1 (1 / 10)
        # ..to time sleep in ms
        # So iteration count now will increase in 10 times.
        if iteration == 30:
            await bot.send_message(
                chat_id=user_id,
                text=TEXTS["states"]["chat"]["wait_too_long"],
                reply_markup=STOP_WAIT,
            )


async def add_user_in_search(*, user_id: str) -> None:
    '''
    Adding user to the list of those who search new chat.

    :param user_id: A string of user's ID
    '''

    if user_id not in users_searching:
        users_searching.append(user_id)


async def start_new_chat(
    *,
    user_id: str,
    bot: Bot,
    dispatcher: Dispatcher,
    state: FSMContext
) -> None:
    '''
    Starting new chat with random user from the waiting list.

    :param user_id: User ID, whose chat we wan't to start
    :param bot: Current bot instance
    :param dispatcher: Current dispatcher instance
    :param state: State of the user
    '''

    # First of all, we need to make sure
    # ..that we don't have any chat's of the user
    current_state = await state.get_state()
    
    if current_state == Chat.loading_chat:
        await bot.send_message(
            chat_id=user_id,
            text=TEXTS["states"]["chat"]["still_searching"]
        )

        return

    await stop_this_chat(
        user_id=user_id,
        bot=bot,
        dispatcher=dispatcher,
        state=state
    )


    # Checking if user is alone in the wait list.
    if len(users_searching) == 0:
        # Make user waiting new chat users
        asyncio.ensure_future(
            coro_or_future=wait_new_chat(
                user_id=user_id,
                bot=bot,
                state=state
            )
        )

        return

    random_user = random.choice(users_searching)
    await add_user_in_search(user_id=user_id)

    # Checking if we got somewho from the searching list
    # And this user is not us
    # If so, make user waiting
    if random_user is None:
        asyncio.ensure_future(
            coro_or_future=wait_new_chat(
                user_id=user_id,
                state=state,
                bot=bot
            )
        )

        return

    # If all checks are good, creating new chat.
    # Start from deleting user and he's companion from searching list.
    del users_searching[users_searching.index(user_id)]
    del users_searching[users_searching.index(random_user)]

    # Converting random_user to int
    # This made because resolve_context function need this,
    # ..but all functions below the resolve_context
    # ..are not actually gives even a little shit to the type of user_id
    random_user = int(random_user)

    companion_state = dispatcher.fsm.resolve_context(
        bot=bot,
        chat_id=random_user,
        user_id=random_user
    )

    await companion_state.set_data({"CURRENT_CHAT": user_id})
    await companion_state.set_state(Chat.private_chat)

    await state.set_data({"CURRENT_CHAT": random_user})
    await state.set_state(Chat.private_chat)

    # Sending to our user's "hooray, we found the chat!" message.
    await bot.send_message(
        chat_id=random_user,
        text=TEXTS["states"]["chat"]["found"]
    )

    await bot.send_message(
        chat_id=user_id,
        text=TEXTS["states"]["chat"]["found"]
    )

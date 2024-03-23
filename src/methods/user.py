from __future__ import annotations

import random
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext


from models.states import Chat
from models import ChatResponse

from config import TEXTS, TIMES
from keyboard import MAIN_MENU, STOP_WAIT
from methods.entertainments import Fact


users_searching: list[User] = []


class User:
    user_id: str
    state: FSMContext = None
    bot: Bot = None
    dispatcher: Dispatcher = None

    def __init__(
        self,
        *,
        user_id: str,
        state: FSMContext = None,
        bot: Bot = None,
        dispatcher: Dispatcher = None
    ) -> None:
        '''
        User abstraction

        :param user_id: ID of the user
        :param state: State of the user
        :param bot: Bot instance
        :param dispatcher: Dispatcher instance
        '''

        self.user_id = user_id
        self.state = state
        self.bot = bot
        self.dispatcher = dispatcher

    def __eq__(self, other: User) -> bool:
        '''
        Special dunder method to check if users objects are equal

        :param other: User to be checked
        '''

        return self.user_id == other.user_id

    async def clear(self) -> None:
        '''
        Clear user chat information and state too

        :param state: State of the user we want to clean.
        :param user_id: User ID
        '''

        if self in users_searching:
            del users_searching[self]

        await self.state.clear()

    async def get_chat(self) -> ChatResponse:
        '''
        Get User of the companion

        :param state: State of the user you want to get chat from.
        :return: Integer, ID of the companion
        if user have current chat and None otherwise.
        '''

        _result = await self.state.get_data()

        current_chat = _result.get("CURRENT_CHAT")

        if current_chat is None:
            return ChatResponse(companion=None)

        return ChatResponse(
            companion=current_chat,
            message_start_id=int(_result.get("START_MESSAGE_ID"))
        )

    async def stop_chat(self) -> None:
        '''
        Stoping current chat by user ID

        :param companion: A user
        :param bot: Instance of current bot.
        :param dispatcher: Instance of current dispatcher.
        :param state: State of the user whose chat we want to stop.
        '''

        chat = await self.get_chat()

        if chat.companion is None:
            return

        await chat.companion.clear()
        await self.clear()

        await self.bot.send_message(
            chat_id=chat.companion.user_id,
            text=TEXTS["states"]["chat"]["finish_by_companion"]
        )

        # So this user is in menu now
        # Sending menu messages to our companion.
        await self.bot.send_message(
            chat_id=chat.companion.user_id,
            text=TEXTS["states"]["menu"]["general"],
            reply_markup=MAIN_MENU
        )

        await self.bot.send_message(
            chat_id=self.user_id,
            text=TEXTS["states"]["chat"]["finish"]
        )

    async def wait_new_chat(self) -> None:
        '''
        Make user wait his new chat by user ID

        :param user_id: ID of user, that we want to be waiting
        :param bot: Bot instance
        :param state: State of the user
        '''

        # Getting seconds times from json
        # Multiply to 10
        # Need additional variable due to E501 error
        TIMES_TOO_LONG = TIMES["wait_too_long"]
        FIRST_MESSAGE_SECONDS = TIMES_TOO_LONG["first_message_seconds"] * 10
        FACT_ITERATION_SECONDS = TIMES_TOO_LONG["fact_iteration_seconds"] * 10

        await self.add_to_search()
        await self.state.set_state(state=Chat.loading_chat)
        await self.bot.send_message(
            chat_id=self.user_id,
            text=TEXTS["states"]["chat"]["search"]
        )

        iteration = 0

        # Checking our state here every 100ms
        # If someone found us and we're in the private chat
        # ..or we canceled searching this loop will'be ended
        while True:
            await asyncio.sleep(0.1)
            iteration += 1

            chat_not_found = await self.state.get_state()

            if chat_not_found == Chat.private_chat or \
                    self not in users_searching:

                break

            if iteration == FIRST_MESSAGE_SECONDS:
                await self.bot.send_message(
                    chat_id=self.user_id,
                    text=TEXTS["states"]["chat"]["wait_too_long"],
                    reply_markup=STOP_WAIT,
                )

            elif iteration % FACT_ITERATION_SECONDS == 0:

                intersting_fact = await Fact.get()

                if not intersting_fact.status:
                    return

                message_text = TEXTS["states"]["chat"]["wait_intersting_fact"]
                message_text += intersting_fact.text

                await self.bot.send_message(
                    chat_id=self.user_id,
                    text=message_text
                )

    async def add_to_search(self) -> None:
        '''
        Add user to the list of those who search new chat.

        :param user_id: A string of user's ID
        '''

        if self.user_id not in users_searching:
            users_searching.append(self)

    async def start_new_chat(self) -> None:
        '''
        Starting new chat with random user from the waiting list.
        '''

        current_state = await self.state.get_state()

        if current_state == Chat.loading_chat:
            await self.bot.send_message(
                chat_id=self.user_id,
                text=TEXTS["states"]["chat"]["still_searching"]
            )

            return

        await self.stop_chat()

        # Checking if user is alone in the wait list.
        if len(users_searching) == 0:
            asyncio.ensure_future(
                coro_or_future=self.wait_new_chat()
            )

            return

        random_user = random.choice(users_searching)
        await self.add_to_search()

        if random_user is None:
            asyncio.ensure_future(
                coro_or_future=self.wait_new_chat()
            )

            return

        del users_searching[users_searching.index(self)]
        del users_searching[users_searching.index(random_user)]

        start_message = await self.bot.send_message(
            chat_id=random_user.user_id,
            text=TEXTS["states"]["chat"]["found"]
        )

        await random_user.state.set_data(
            {
                "CURRENT_CHAT": self,
                "START_MESSAGE_ID": start_message.message_id
            }
        )

        await random_user.state.set_state(Chat.private_chat)

        start_message = await self.bot.send_message(
            chat_id=self.user_id,
            text=TEXTS["states"]["chat"]["found"]
        )

        await self.state.set_data({
                "CURRENT_CHAT": random_user,
                "START_MESSAGE_ID": start_message.message_id
            }
        )

        await self.state.set_state(Chat.private_chat)

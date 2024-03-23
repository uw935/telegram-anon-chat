import time
import asyncio

from loguru import logger

from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, ReactionTypeEmoji

from db import session
from keyboard import MAIN_MENU
from db.models.users import User
from config import TEXTS, BOT_TOKEN

from handlers.menu import router as menu_router
from handlers.chat import router as chat_router

from sqlalchemy.exc import OperationalError


dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    '''
    Handler to the "/start" command.

    :param message: Telergam Message
    '''

    await message.react([ReactionTypeEmoji(emoji="👍")])

    db = session()

    try:
        user = db.query(User).filter(User.user_id == message.chat.id).first()
    except OperationalError:
        logger.error(
            "It looks like you doesn't created users.db. "
            "Read contributing from the README.md file to create one"
        )

        return

    if user is None:
        logger.info(
            f"New user just wrote: "
            f"username: @{message.from_user.username} "
            f"| fullname: {message.from_user.full_name} "
            f"| ID: {message.from_user.id}"
        )

        user = User(
            user_id=message.from_user.id,
            username=message.from_user.username,
            fullname=message.from_user.full_name,
            timestamp=int(time.time()),
        )

        try:
            db.add(user)
            db.commit()
            db.refresh(user)
        except Exception as e:
            db.rollback()
            logger.exception(e)

    db.close()

    await message.answer(text=TEXTS["states"]["start"])
    await message.answer(
        text=TEXTS["states"]["menu"]["general"],
        reply_markup=MAIN_MENU
    )


@dp.startup()
async def on_startup_handler() -> None:
    '''
    Startup event handler
    '''

    logger.info("Application just started")


@dp.shutdown()
async def on_shutdown_handler() -> None:
    '''
    Shutdown event handler
    '''

    logger.info("Application shuted down, goodbye!")


async def main() -> None:
    logger.info("Initializing application")

    dp.include_router(menu_router)
    dp.include_router(chat_router)

    await dp.start_polling(Bot(token=BOT_TOKEN))


if __name__ == "__main__":
    asyncio.run(main())

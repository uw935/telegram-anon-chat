import time
import asyncio

from aiogram import Dispatcher, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import Message

from loguru import logger
from config import TEXTS, BOT_TOKEN
from db.models.users import User
from db import session

from routers.menu import router as menu_router
from routers.chat.chat import router as chat_router


dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:

    db = session()
    user = db.query(User).filter(User.user_id == message.chat.id).first()

    if user is None:
        logger.info(
            f"New user just wrote: username: | {message.from_user.username} | fullname: {message.from_user.full_name} | ID: {message.from_user.id}"
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

    await message.answer(TEXTS["states"]["start"])
    

@dp.startup()
async def on_startup() -> None:
    logger.info("Application just started")


@dp.shutdown()
async def on_shutdown() -> None:
    logger.info("Application shuted down, goodbye!")


async def main() -> None:
    logger.info("Initializing application")

    dp.include_router(menu_router)
    dp.include_router(chat_router)

    await dp.start_polling(
        Bot(token=BOT_TOKEN)
    )


if __name__ == "__main__":
    asyncio.run(main())

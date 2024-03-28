import asyncio

from loguru import logger

from aiogram import Dispatcher, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, ReactionTypeEmoji

from db import add_user_to_db
from keyboard import MAIN_MENU
from config import TEXTS, BOT_TOKEN

from handlers.menu import router as menu_router
from handlers.chat import router as chat_router


dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message, bot: Bot) -> None:
    '''
    Handler to the "/start" command.

    :param message: Telergam Message
    '''

    await message.react([ReactionTypeEmoji(emoji="👍")])

    is_user_added = await add_user_to_db(
        user_id=message.from_user.id,
        username=message.from_user.username,
        fullname=message.from_user.full_name,
        bot=bot
    )

    if is_user_added:
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

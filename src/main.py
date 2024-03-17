import time
import asyncio

from loguru import logger

from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import TEXTS, bot
from db.models.users import User
from db import session
from states import Chat

from routers.menu import router as menu_router
from routers.chat import router as chat_router
from routers.menu.keyboard import MAIN_MENU


dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    db = session()
    user = db.query(User).filter(User.user_id == message.chat.id).first()
    
    if user is None:
        user = User(
            user_id=message.from_user.id,
            username=message.from_user.username,
            fullname=message.from_user.full_name,
            timestamp=int(time.time())
        )

        try:
            db.add(user)
            db.commit()
            db.refresh(user)
        except Exception as e:
            db.rollback()
            logger.exception(e)            

    await state.set_state(Chat.menu)
    await message.answer(TEXTS["states"]["start"])


async def main() -> None:
    dp.include_router(menu_router)
    dp.include_router(chat_router)
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from config import TOKEN, TEXTS

from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import Message

from routers import menu
from states import StartChat


dp = Dispatcher()
dp.include_router(menu.router)


@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext) -> None:
    state.set_state(StartChat.menu)
    await message.reply(TEXTS["states"]["start"])


async def main() -> None:
    await dp.start_polling(
        Bot(token=TOKEN)
    )


if __name__ == "__main__":
    asyncio.run(main())


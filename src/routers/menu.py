from aiogram import Router
from aiogram.types import Message

from states import StartChat
from config import TEXTS


router = Router()


@router.message(StartChat.menu)
async def menu(message: Message):
    await message.reply(TEXTS["menu"]["general"])



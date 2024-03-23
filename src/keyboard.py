from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


MAIN_MENU = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💫 Start new chat",
                callback_data="START_NEW_CHAT"
            )
        ]
    ]
)

STOP_WAIT = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🛑 Stop searching",
                callback_data="STOP_SEARCH"
            )
        ],
    ]
)

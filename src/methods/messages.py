import re

from models import ChatResponse
from config import AVAILABLE_TYPES
from aiogram.types import ContentType


regex = re.compile(
    r"^(?:http|ftp)s?://"
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+"
    r"(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
    r"localhost|"
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    r"(?::\d+)?"
    r"(?:/?|[/?]\S+)$|"
    r"(@[A-Za-z0-9])",
    re.IGNORECASE
)


class Message:
    # async def get_message_reply_id(
    #     *,
    #     message_id: int,
    #     sender: ChatResponse,
    # ) -> int:
    #     companion_chat = await sender.companion.get_chat()

    # TODO : calculate the reply_id

    #     a = (message.reply_to_message.message_id - chat.message_start_id)

    #     logger.debug((a, companion_chat.message_start_id + a))


    @staticmethod
    async def is_valide_message(
        *,
        message: str,
        message_type: ContentType
    ) -> bool:
        '''
        Predict function to check if this message is valide

        :param message: Message to check
        :param messag_type: Telegram type of this message
        :return: Bool, True if message valide, False otherwise
        '''

        if message_type not in AVAILABLE_TYPES:
            return False

        if message is not None:
            message = message.split()

            for word in message:
                if re.match(regex, word) is not None:
                    return False

        return True

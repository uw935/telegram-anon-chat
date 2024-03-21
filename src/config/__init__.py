import os
import json
import dotenv

from loguru import logger
from aiogram.types import ContentType


logger.add(
    sink="./log/debug.log",
    level="DEBUG",
    rotation="1 MB",
    format="[{time}][{level}]: {message} (line: {line})",
    compression="zip",
    delay=True,
    catch=True,
    diagnose=True,  # set to false on prod
)

dotenv.load_dotenv(dotenv.find_dotenv(".env"))

AVAILABLE_TYPES = [
    ContentType.TEXT,
    ContentType.PHOTO,
    ContentType.STICKER,
    ContentType.VIDEO,
    ContentType.AUDIO,
    ContentType.VOICE,
    ContentType.VIDEO_NOTE
]

BOT_TOKEN = os.environ["BOT_TOKEN"]
TEXTS = json.load(open("config/answers.json", "r", encoding="UTF-8"))
DB_URL = os.environ["DB_URL"]

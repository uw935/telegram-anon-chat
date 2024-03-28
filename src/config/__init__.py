import os
import json
import dotenv

from loguru import logger
from aiogram.types import ContentType


logger.add(
    sink="./log/debug.log",
    level="INFO",
    rotation="1 MB",
    format="[{time}][{level}]: {message} (line: {line})",
    compression="zip",
    delay=True,
    catch=True,
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

DB_URL = os.environ["DB_URL"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
OWNER_CHAT_ID = os.environ["OWNER_CHAT_ID"]
TIMES = json.load(open("config/json/times.json", "r", encoding="UTF-8"))
TEXTS = json.load(open("config/json/answers.json", "r", encoding="UTF-8"))
INTERESTING_FACTS_API = "https://uselessfacts.jsph.pl/api/v2/facts/random"

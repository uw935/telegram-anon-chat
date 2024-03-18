import os
import json
import dotenv
from aiogram import Bot
from loguru import logger


dotenv.load_dotenv(dotenv.find_dotenv(".env"))

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

BOT_TOKEN = os.environ["BOT_TOKEN"]
TEXTS = json.load(open("config/answers.json", "r", encoding="UTF-8"))
DB_URL = os.environ["DB_URL"]

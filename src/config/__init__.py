import os
import json
import dotenv
from aiogram import Bot


dotenv.load_dotenv(dotenv.find_dotenv(".env"))

bot = Bot(token=os.environ["BOT_TOKEN"])
TEXTS = json.load(open("config/answers.json", "r", encoding="UTF-8"))
DB_URL = os.environ["DB_URL"]

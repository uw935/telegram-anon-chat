import os
import json
import dotenv


dotenv.load_dotenv()
TOKEN = os.environ["BOT_TOKEN"]
TEXTS = json.load(open("config/answers.json", "r", encoding="UTF-8"))

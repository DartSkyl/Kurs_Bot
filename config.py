import os
from dotenv import load_dotenv, find_dotenv
import logging


if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('bot_token')
WEBHOOK = os.getenv('webhook_url')

logging.basicConfig(
    filename='bot.log',
    filemode='a',
    format="%(asctime)s %(levelname)s %(message)s"
)
logging.getLogger().setLevel(logging.ERROR)

import os
from dotenv import load_dotenv

from services.connection import bot

load_dotenv()


async def on_shutdown(x):
    await bot.send_message(int(os.getenv('admin_tg')), '🟥 The bot turned off')


async def on_startup(x):
    await bot.send_message(int(os.getenv('admin_tg')), '🟩 The bot turned on')

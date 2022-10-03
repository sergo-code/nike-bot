import os
from dotenv import load_dotenv

from db.db import PostgreSQL

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


load_dotenv()

bot = Bot(token=os.getenv('token'))
dp = Dispatcher(bot, storage=MemoryStorage())
database = PostgreSQL()

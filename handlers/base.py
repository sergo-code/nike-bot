from aiogram import types, Dispatcher
from aiogram.utils.markdown import hbold

from services.connection import database
from keyboards.keyboard import admin, user, TextButtonList
from services.check_user import is_admin
from services.get_profile import info_profile
from services.get_subscribers import subscription


async def start(message: types.Message):
    if not bool(database.select(f'SELECT * FROM profile WHERE telegram_id = {message.from_id}').fetchone()):
        database.insert(table='profile', insert='telegram_id', value=message.from_id)
    keyboard = admin if await is_admin(message.chat.id) else user
    text = "Good day!\n" \
           "To interact with the bot, use the additional keyboard."
    await message.answer(text, reply_markup=keyboard)


async def about(message: types.Message):
    text = f'{hbold("Nike Sale Service")}\n\n' \
           'It will help to save on the purchase, if you think about it in advance.\n\n' \
           '1. Сlick ➕ Add a product.\n' \
           '2. Send the bot a link to an available product.\n' \
           '3. Choose the size you are interested in.\n' \
           '4. Subscribe.\n\n' \
           '- The bot will notify you if the price drops and your size is available.\n' \
           '- The bot will also notify you if your size is unavailable.\n\n' \
           'Then the subscription will be canceled automatically in both cases.'
    await message.answer(text, parse_mode='html')


async def feedback(message: types.Message):
    await message.answer('@offliny')


async def profile(message: types.Message):
    await info_profile(message)


async def subscribers(message: types.Message):
    await subscription(message)


def register_handler_base(dp: Dispatcher):
    dp.register_message_handler(start, commands="start")
    dp.register_message_handler(profile, text=[TextButtonList['profile']])
    dp.register_message_handler(subscribers, text=[TextButtonList['subscribers']])
    dp.register_message_handler(about, text=[TextButtonList['about']])
    dp.register_message_handler(feedback, text=[TextButtonList['feedback']])

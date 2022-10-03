from aiogram import types, Dispatcher

from keyboards.keyboard import TextButtonList
from services.check_user import is_admin
from services.get_subscribers import subscription
from services.get_info_users import info_users
from services.connection import database


async def info_users_(message: types.Message):
    if await is_admin(message.from_id):
        await info_users(message)


async def users(message: types.Message):
    if await is_admin(message.from_id):
        telegram_id = message.text.split()[1]
        await subscription(message, telegram_id)


async def limit(message: types.Message):
    if await is_admin(message.from_id):
        telegram_id, max_sub = message.text.split()[1:]
        database.update('profile', 'max_sub', max_sub, 'telegram_id', telegram_id)
        text = f'Data for user {telegram_id} has been updated!'
        await message.answer(text)


def register_handler_admin(dp: Dispatcher):
    dp.register_message_handler(users, commands=['user'])
    dp.register_message_handler(info_users_, text=[TextButtonList['info_users']])
    dp.register_message_handler(limit, commands=['limit'])

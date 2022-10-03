from aiogram import types
from aiogram.utils.markdown import hbold, hcode

from services.connection import database


async def info_users(message: types.Message):
    request = "SELECT subscribers.telegram_id, COUNT(*), profile.max_sub " \
              "FROM subscribers " \
              "JOIN profile ON subscribers.telegram_id=profile.telegram_id " \
              "GROUP BY subscribers.telegram_id, profile.max_sub"
    subs = database.select(request).fetchall()

    if bool(subs):
        text = f'{hbold("[INFO]")}\n'
        text += f'➖➖➖➖➖➖➖➖➖\n'
        for sub in subs:
            text += f'{hcode(sub[0])} - {sub[1]}/{sub[2]}\n'
            text += f'➖➖➖➖➖➖➖➖➖\n'
        await message.answer(text, parse_mode='html')
    else:
        await message.answer('There are no subscriptions')

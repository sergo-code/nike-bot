from aiogram import types
from aiogram.utils.markdown import hbold, hcode

from services.connection import database


async def info_profile(message: types.Message):
    subscribe = database.select(f'SELECT COUNT(*), max_sub FROM subscribers '
                                f'JOIN profile ON profile.telegram_id=subscribers.telegram_id '
                                f'WHERE profile.telegram_id = {message.from_id} '
                                f'GROUP BY profile.max_sub').fetchone()
    count_sub = str(subscribe[0]) if bool(subscribe) else 0
    max_sub = str(subscribe[1]) if bool(subscribe) else 5

    text = f"{hbold('Profile')}\n" \
           f"➖➖➖➖➖➖➖➖➖\n" \
           f"🔑 {hbold('ID')}: {hcode(str(message.from_user.id))}\n" \
           f"⚙ {hbold('Subscription limit')}: {hcode(count_sub)} / {hcode(max_sub)}\n" \
           f"➖➖➖➖➖➖➖➖➖"

    await message.answer(text, parse_mode='html')

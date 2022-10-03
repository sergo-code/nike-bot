from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hbold, hlink, hitalic, hcode

from services.connection import database


async def subscription(message: types.Message, telegram_id=None):
    if telegram_id is None:
        telegram_id = message.from_id
    subs = database.select(f'SELECT '
                           f'nike.title, nike.seller, nike.url, nike.product_type, '
                           f'subscribers.id, subscribers.size, subscribers.price '
                           f'FROM subscribers '
                           f'INNER JOIN nike ON subscribers.product_id=nike.cloud_product_id '
                           f'INNER JOIN profile ON subscribers.telegram_id = profile.telegram_id '
                           f'WHERE subscribers.telegram_id = {telegram_id}').fetchall()

    if bool(subs):
        text = f'{hbold("✅ Subscriptions")}\n\n'
        reply_markup = InlineKeyboardMarkup()

        for i in range(len(subs)):
            reply_markup.insert(InlineKeyboardButton(text=f'{i + 1}', callback_data=f"delete:{subs[i][4]}"))
            text += '➖➖➖➖➖➖➖➖➖➖➖➖\n'
            if subs[i][3] == 'FOOTWEAR':
                emoji = '👟'
            elif subs[i][3] == 'APPAREL':
                emoji = '👘'
            else:
                emoji = '🛍️'

            text += f'{emoji} {hlink(subs[i][0], subs[i][2])}\n' \
                    f'🏷️ {hitalic(subs[0][1])}\n' \
                    f'💰 Price: {hcode(subs[i][6])} {hcode("$")}\n' \
                    f'📏 Size: {hcode(subs[i][5])}\n' \
                    f'🔕 Cancel subscription 👉 {i+1}\n'

        text += '➖➖➖➖➖➖➖➖➖➖➖➖\n\n'
        text += f'{hitalic("Price - the price fixed at the time of subscription")}'

        await message.answer(text, reply_markup=reply_markup, disable_web_page_preview=True, parse_mode='html')
    else:
        text = "⛔ You don't have any active subscriptions."
        await message.answer(text, parse_mode='html')

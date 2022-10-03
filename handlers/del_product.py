from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from services.connection import database, bot


async def del_subscribe(call: types.CallbackQuery):
    nike_id = call.data.split(':')[1]
    request = f"SELECT product_id FROM subscribers WHERE id='{nike_id}'"
    if bool(database.select(request).fetchone()):
        database.delete('subscribers', 'id', f"'{nike_id}'")
        await call.message.delete()
        text = 'The subscription was successfully deleted.'
        await bot.send_message(call.from_user.id, text=text)
    else:
        text = 'Subscription not found, refresh the list and try again.'
        await bot.send_message(call.from_user.id, text=text)


def register_handler_del_subscribe(dp: Dispatcher):
    dp.register_callback_query_handler(del_subscribe, Text(startswith='delete:'))

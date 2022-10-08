from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.markdown import hcode, hbold, hitalic, hstrikethrough

from services.connection import database, bot
from keyboards.keyboard import TextButtonList
from nike.get_product import get_item


class AddProduct(StatesGroup):
    product = State()


async def message_product(message, data):
    text = f"{hbold(data['title'])}\n" \
           f"{hitalic(data['seller'])}\n"
    if not data['discounted']:
        text += f"Price: {hcode(data['current_price'])} $"
    else:
        text += f"Price: {hcode(data['current_price'])} $ {hstrikethrough(data['full_price'])} $"
    sizes = data['size']
    reply_markup = types.InlineKeyboardMarkup()

    request = "SELECT id FROM nike WHERE cloud_product_id='{}'".format(data['cloud_product_id'])
    id_ = database.select(request).fetchone()[0]

    for size in sizes:
        callback_data = f"size:{size}:{id_}:{data['current_price']}"
        reply_markup.insert(types.InlineKeyboardButton(text=f"{size}", callback_data=callback_data))
    await bot.send_photo(message.from_user.id, data['image_url'], text, reply_markup=reply_markup, parse_mode='html')


async def add_product(message: types.Message):
    if not bool(database.select(f'SELECT * FROM profile WHERE telegram_id = {message.from_id}').fetchone()):
        database.insert(table='profile', insert='telegram_id', value=message.from_id)
    await AddProduct.product.set()
    text = 'Enter the link to the product you are interested in.'
    await message.answer(text)


async def set_link(message: types.Message, state=FSMContext):
    if 'https://www.nike.com/' in message.text and \
            len(message.text.split('/')) == 7 or \
            len(message.text.split('/')) == 6:

        data = await get_item(message.text)
        if data:
            request = "SELECT cloud_product_id FROM nike WHERE cloud_product_id='{}'".format(data['cloud_product_id'])
            if not bool(database.select(request).fetchone()):
                # Отправка данных в таблицу nike
                insert = 'cloud_product_id, title, url, product_type, seller'
                value = "'{cloud_product_id}', '{title}', '{url}', '{product_type}', '{seller}'".format(
                    cloud_product_id=data['cloud_product_id'],
                    title=data['title'],
                    url=data['url'],
                    product_type=data['product_type'],
                    seller=data['seller'])
                database.insert(table='nike', insert=insert, value=value)
            await message_product(message, data)
        else:
            text = 'Invalid link specified!'
            await message.answer(text)
    else:
        text = 'Invalid link specified!'
        await message.answer(text)
    await state.finish()


async def set_size(call: types.CallbackQuery):
    size, nike_id, price = call.data.split(':')[1:]
    await call.answer(f"You have chosen size {size}!")
    reply_markup = InlineKeyboardMarkup()
    callback_data = f"accept:{size}:{nike_id}:{price}"
    reply_markup.add(InlineKeyboardButton(text=f"Confirm {size} size", callback_data=callback_data))
    reply_markup.add(InlineKeyboardButton(text='Cancel', callback_data=f"cancel"))
    await call.message.edit_reply_markup(reply_markup=reply_markup)


async def set_cancel(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup())


async def set_accept(call: types.CallbackQuery):
    # Number of current subscriptions
    request = "SELECT COUNT(*) FROM subscribers WHERE telegram_id={telegram_id}".format(telegram_id=call.from_user.id)
    count_sub = database.select(request).fetchone()[0]
    # Maximum number of subscriptions for a profile
    request = "SELECT max_sub FROM profile WHERE telegram_id={telegram_id}".format(telegram_id=call.from_user.id)
    max_sub = database.select(request).fetchone()[0]
    if count_sub < max_sub:
        size, nike_id, price = call.data.split(':')[1:]

        request = "SELECT product_type, title, cloud_product_id FROM nike WHERE id={}".format(nike_id)
        data = database.select(request).fetchone()

        if data[0] == 'FOOTWEAR':
            emoji = '👟'
        elif data[0] == 'APPAREL':
            emoji = '👚'
        else:
            emoji = '🛍️'

        text = f'✅ {hbold("You have subscribed")}\n' \
               f'{emoji} {data[1]}\n' \
               f'📏 Size: {hcode(size)}\n' \
               f'💰 Price: {hcode(price)} {hcode("$")}\n'

        # Sending data to the subscribers table
        insert = "telegram_id, product_id, size, price"
        values = "{telegram_id}, '{cloud_product_id}', '{size}', {price}".format(
            telegram_id=call.from_user.id,
            cloud_product_id=data[2],
            size=size,
            price=price)

        database.insert(table='subscribers', insert=insert, value=values)

    else:
        text = f'All subscription slots are occupied.\n{count_sub}/{max_sub}'
    await call.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup())
    await call.message.answer(text, parse_mode='html')


def register_handler_add_product(dp: Dispatcher):
    dp.register_message_handler(add_product, text=[TextButtonList['add_product']])
    dp.register_message_handler(set_link, content_types=["text"], state=AddProduct.product)
    dp.register_callback_query_handler(set_size, Text(startswith='size:'))
    dp.register_callback_query_handler(set_cancel, text='cancel')
    dp.register_callback_query_handler(set_accept, Text(startswith='accept:'))

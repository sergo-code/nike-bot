import asyncio

from aiogram.utils.markdown import hbold, hlink, hcode

from services.connection import database, bot
from nike.get_product import get_item


async def up():
    while True:
        # Displays unique links to products in the subscriptions table
        request = "SELECT DISTINCT nike.url FROM subscribers JOIN nike ON subscribers.product_id=nike.cloud_product_id"
        links = database.select(request).fetchall()
        data = list()
        for link in links:
            data.append(await get_item(link[0]))
        for i in range(len(data)):
            request = "SELECT telegram_id, size, price FROM subscribers WHERE product_id='{}'".format(data[i]['cloud_product_id'])
            subs = database.select(request).fetchall()
            for sub in subs:
                if data[i]['product_type'] == 'FOOTWEAR':
                    emoji = '👟'
                elif data[i]['product_type'] == 'APPAREL':
                    emoji = '👚'
                else:
                    emoji = '🛍️'
                if sub[1] in data[i]['size']:
                    if sub[2] < int(data[i]['current_price']):
                        text = f"🔥 {hbold('The price has dropped')} 🔥\n\n"\
                               f"➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                               f"{emoji} {hlink(data[i]['title'], data[i]['url'])}\n"\
                               f"📏 Size: {hcode(sub[1])}\n"\
                               f"💰 Old price: {hcode(sub[2])} $\n"\
                               f"🤑 New price: {hcode(data[i]['current_price'])} $\n" \
                               f"➖➖➖➖➖➖➖➖➖➖➖➖"
                        await del_subscribe(data[i]['cloud_product_id'])
                        await bot.send_message(sub[0], text=text, disable_web_page_preview=True, parse_mode='html')
                else:
                    text = f"🛑 {hbold('Sold out size')} 🛑\n\n" \
                           f"➖➖➖➖➖➖➖➖➖➖➖➖\n" \
                           f"{emoji} {hlink(data[i]['title'], data[i]['url'])}\n" \
                           f"📏 Size: {sub[1]}\n"\
                           f"💰 Price: {hcode(sub[2])} $\n" \
                           f"➖➖➖➖➖➖➖➖➖➖➖➖"

                    await del_subscribe(data[i]['cloud_product_id'])
                    await bot.send_message(sub[0], text=text, disable_web_page_preview=True, parse_mode='html')
        await asyncio.sleep(2*60)


async def del_subscribe(cloud_product_id):
    database.delete('subscribers', 'product_id', f"'{cloud_product_id}'")

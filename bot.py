from services.connection import dp
from handlers import base, add_product, del_product, admin
from services.power_switch_message import on_startup, on_shutdown
from aiogram import executor
from nike import updater

import asyncio


base.register_handler_base(dp)
add_product.register_handler_add_product(dp)
del_product.register_handler_del_subscribe(dp)
admin.register_handler_admin(dp)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(updater.up())

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)

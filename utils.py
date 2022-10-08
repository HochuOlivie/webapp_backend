import asyncio
from asgiref.sync import sync_to_async
from aiogram import Bot
from aiogram import types


async def delete_order_on_timeout(bot, message: types.Message, order):
    Bot.set_current(bot)
    await asyncio.sleep(60 * 60)
    await message.edit_text("Заказ был автоматически удален по истечению срока давности")
    await sync_to_async(order.delete)()

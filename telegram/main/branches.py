import logging

from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from asgiref.sync import sync_to_async

from db.models import User, Order, Offer
from initialize import url
from aiogram.dispatcher import FSMContext


class Main:
    def __init__(self, bot, dp):
        self.bot: Bot = bot
        self.dp: Dispatcher = dp

    def register_commands(self):
        ...

    def register_handlers(self):
        ...
        # self.dp.register_message_handler(self._contact_handler, content_types=['contact'], state=States.phone)
        # self.dp.register_message_handler(self._name_handler, state=States.name)
        self.dp.register_callback_query_handler(self._delete_order, text_startswith='order_delete', state="*")
        self.dp.register_callback_query_handler(self._delete_offer, text_startswith='offer_delete', state="*")
        self.dp.register_callback_query_handler(self._accept_order, text_startswith='order_accept', state="*")
        self.dp.register_callback_query_handler(self._decline_order, text_startswith='order_decline', state="*")

    async def _delete_order(self, callback: types.CallbackQuery):
        _, order_id = callback.data.split(':')
        await sync_to_async((await Order.objects.aget(id=order_id)).delete)()
        await callback.message.edit_text('Курьеры больше не будут видеть ваш заказ')

    async def _delete_offer(self, callback: types.CallbackQuery):
        _, offer_id = callback.data.split(':')
        await sync_to_async((await Offer.objects.aget(id=offer_id)).delete)()
        await callback.message.edit_text('Заказчики больше не будут видеть ваше предложение')

    async def _accept_order(self, callback: types.CallbackQuery):
        _, order_id = callback.data.split(':')
        order = await Order.objects.aget(id=order_id)
        await callback.message.edit_text(f'Контакт: @{order.user.tg_username}')
        await self.bot.send_message(order.user.tg_id, f'Партнер согласился на доставку\n\nКонтакт: @{callback.from_user.username}')

    async def _decline_order(self, callback: types.CallbackQuery):
        _, order_id = callback.data.split(':')
        order = await Order.objects.aget(id=order_id)
        await callback.message.edit_text(f'Вы отказались от заказа')

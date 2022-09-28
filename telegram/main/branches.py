from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardMarkup, WebAppInfo

from db.models import User, Order, Offer
from initialize import url
from aiogram.dispatcher import FSMContext


class Registration:
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

    def _delete_order(self, callback: types.CallbackQuery):
        _, order_id = callback.data.split(':')
        Order.objects.get(id=order_id).delete()
        callback.message.edit_text('Курьеры больше не будут видеть ваш заказ')

    def _delete_offer(self, callback: types.CallbackQuery):
        _, offer_id = callback.data.split(':')
        Offer.objects.get(id=offer_id).delete()
        callback.message.edit_text('Заказчики больше не будут видеть ваше предложение')

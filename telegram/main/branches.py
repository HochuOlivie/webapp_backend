import logging

from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardMarkup, WebAppInfo, InlineKeyboardButton
from asgiref.sync import sync_to_async

from db.models import User, Order, Offer, CustomerReview, PartnerReview
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
        self.dp.register_callback_query_handler(self._rate_finish, text_startswith='rate_submit', state="*")
        self.dp.register_callback_query_handler(self._rate, text_startswith='rate', state="*")
        self.dp.register_inline_handler(self._choose_addr, state="*")

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
        try:
            order = await Order.objects.aget(id=order_id)
        except:
            await callback.message.edit_text("Заказ уже неактуален")
            return
        await callback.message.edit_text(f'Контакт: @{order.user.tg_username}', reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("⭐️ Оценить заказчика", callback_data=f'rate:customer:{order.user.tg_id}'),
        ))
        await self.bot.send_message(order.user.tg_id, f'Партнер согласился на доставку\n\nКонтакт: @{callback.from_user.username}',
                                    reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("⭐️ Оценить партнера", callback_data=f'rate:partner:{callback.from_user.id}'),
        ))

    async def _decline_order(self, callback: types.CallbackQuery):
        _, order_id = callback.data.split(':')
        try:
            order = await Order.objects.aget(id=order_id)
        except:
            await callback.message.edit_text("Заказ уже неактуален")
            return
        await callback.message.edit_text(f'Вы отказались от заказа')

    async def _rate(self, callback: types.CallbackQuery):
        _, type, tg_id = callback.data.split(':')
        user = await User.objects.aget(tg_id=tg_id)
        kb = None
        if type == 'partner':
            kb = InlineKeyboardMarkup()
            for i in range(1, 6):
                kb.add(
                    InlineKeyboardButton("⭐️" * i, callback_data=f'rate_submit:partner:{i}:{tg_id}'),
                )
        elif type == 'customer':
            kb = InlineKeyboardMarkup()
            for i in range(1, 6):
                kb.add(
                    InlineKeyboardButton("⭐️" * i, callback_data=f'rate_submit:customer:{i}:{tg_id}'),
                )
        await callback.message.edit_text(f'Отзыв пользователю @{user.tg_username}', reply_markup=kb)

    async def _rate_finish(self, callback: types.CallbackQuery):
        _, type, points, tg_id = callback.data.split(':')
        user = await User.objects.aget(tg_id=tg_id)
        if type == 'partner':
            await sync_to_async(PartnerReview.objects.create)(user=user, points=points)
        elif type == 'customer':
            await sync_to_async(CustomerReview.objects.create)(user=user, points=points)
        await callback.message.edit_text(f'Отзыв пользователю @{user.tg_username}\n\n{"⭐" * int(points)}️')

    async def _choose_addr(self, query: types.InlineQuery):
        text = query.query
        logging.debug(text)
        return await query.answer([types.InlineQueryResultArticle(
            id=text,
            title=text,
            input_message_content=text,
            )],
            is_personal=True
        )
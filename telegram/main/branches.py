import logging
from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardMarkup, WebAppInfo, InlineKeyboardButton
from asgiref.sync import sync_to_async
from db.models import User, Order, Offer, CustomerReview, PartnerReview
from initialize import url
from aiogram.dispatcher import FSMContext
import requests
import asyncio
from utils import delete_order_on_timeout
from telegram.state import States


class Main:
    def __init__(self, bot, dp):
        self.bot: Bot = bot
        self.dp: Dispatcher = dp

    def register_commands(self):
        ...

    def register_handlers(self):
        ...
        self.dp.register_callback_query_handler(self._delete_order, text_startswith='order_delete', state="*")
        self.dp.register_callback_query_handler(self._delete_offer, text_startswith='offer_delete', state="*")
        self.dp.register_callback_query_handler(self._accept_order, text_startswith='order_accept', state="*")
        self.dp.register_callback_query_handler(self._decline_order, text_startswith='order_decline', state="*")
        self.dp.register_callback_query_handler(self._rate_finish, text_startswith='rate_submit', state="*")
        self.dp.register_callback_query_handler(self._rate, text_startswith='rate', state="*")
        self.dp.register_inline_handler(self._choose_addr, state="*")
        self.dp.register_message_handler(self._confirm_order, state=States.choose_address)

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

    async def _choose_addr(self, query: types.InlineQuery, state: FSMContext):
        state_data = await state.get_data()
        city = state_data['city']
        text = query.query
        res = requests.get(f'https://suggest-maps.yandex.ru/suggest-geo?callback=&apikey=4240729e-72a9-4ece-815e-704470532e85&v=5&search_type=tp&part={city},{text}&lang=ru_RU&n=5&origin=jsapi2Geocoder&bbox=-180%2C-90%2C180%2C90').json()[1]
        suggestions = [
            types.InlineQueryResultArticle(id=f'{query.id}{id}',
                                           title=i[1],
                                           input_message_content=types.InputTextMessageContent(
                                               message_text=f"<b>{i[1]}</b>",
                                               parse_mode="HTML"
                                           ))
            for id, i in enumerate(res[:5])
        ]
        return await query.answer(suggestions, is_personal=True)

    async def _confirm_order(self, message: types.Message, state: FSMContext):
        state_data = await state.get_data()
        data = state_data['data']
        name = data['properties']['name']
        street = data['properties']['description']
        user = await User.objects.filter(tg_id=message.from_user.id).afirst()
        order = await sync_to_async(Order.objects.create)(feature_from=data, user=user)
        m = await self.bot.send_message(user.tg_id,
                                   f'📦 Ждём, пока кто-нибудь из партнеров примет заказ\n\n'
                                   f'📍 Место <b>{name}</b>\n'
                                   f'🏢 Адрес магазина <b>{street}</b>\n'
                                   f'🏠 Адрес доставки <b>{message.text}</b>\n\n'
                                   f'Партнер, который примет заказ, появится в текущем чате\n\n'
                                   f'Заказ будет автоматически удалён через 1 час',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton("❌ Отменить заказ",
                                                            callback_data=f'order_delete:{order.id}')
                                   ),
                                   parse_mode='HTML')
        asyncio.create_task(delete_order_on_timeout(self.bot, m, order))

        offers = Offer.objects.filter(feature_from__geometry__coordinates=data['geometry']['coordinates'])
        async for offer in offers:
            m = await self.bot.send_message(offer.user.tg_id,
                                       f'Поступил заказ\n\n'
                                       f'🏠 Адрес доставки <b>{message.text}</b>',
                                       reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                           InlineKeyboardButton("✅ Принять", callback_data=f'order_accept:{order.id}'),
                                           InlineKeyboardButton("❌ Отклонить",
                                                                callback_data=f'order_decline:{order.id}')
                                       ),
                                       parse_mode='HTML')
        await state.finish()

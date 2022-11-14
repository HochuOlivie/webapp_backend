from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardMarkup, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from asgiref.sync import sync_to_async

from db.models import User, PartnerReview, CustomerReview
from initialize import url
from . import keyboards
from . import callback_consts as cbc
from aiogram.dispatcher import FSMContext
from .state import States
from django.db.models import Avg


class Registration:
    def __init__(self, bot, dp):
        self.bot: Bot = bot
        self.dp: Dispatcher = dp

    def register_commands(self):
        ...
        self.dp.register_message_handler(self._start_handler, commands=["start"], state="*")
        self.dp.register_message_handler(self._profile_handler, text="🗺 Профиль", state="*")

    def register_handlers(self):
        ...
        self.dp.register_message_handler(self._contact_handler, content_types=['contact'], state=States.phone)

        # self.dp.register_callback_query_handler(self._contact_handler, text=cbc.phone, state="*")

    async def _start_handler(self, message: types.Message):
        if User.objects.filter(tg_id=message.from_user.id).exists():
            await self.bot.send_message(message.from_user.id, "Сделать заказ или доставить",
                                        reply_markup=InlineKeyboardMarkup()
                                        .add(
                                            InlineKeyboardMarkup(text="Открыть карту",
                                                                 web_app=WebAppInfo(url=url)
                                                                 )
                                        )
                                        )
            return
        msg = '''Привет 👋
Это бот для заказа продуктов из любых магазинов, где каждый может выступать как в роли курьера, так и в роли заказчика.
Для продолжения необходимо пройти короткую регистрацию. Нажмите кнопку, чтобы поделиться номером телефона'''
        phone_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        phone_button = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
        phone_keyboard.add(phone_button)

        await self.bot.send_message(message.from_user.id, msg, reply_markup=phone_keyboard)
        await States.phone.set()

    async def _contact_handler(self, message: types.Message, state: FSMContext):
        msg = 'Теперь вы можете кликнуть на свой <b>Профиль</b>, ' \
              'открыть карту и сделать заказ или предложение на доставку из любого места в своем городе'

        phone = message.contact.phone_number

        User.objects.create(
            tg_id=message.from_user.id,
            tg_username=message.from_user.username,
            phone=phone,
        )

        await state.update_data(phone=phone)
        await self.bot.send_message(message.from_user.id, msg,
                                    reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                                        KeyboardButton("🗺 Профиль")
                                    ),
                                    parse_mode='HTML',
                                    )
        await self.bot.send_message(message.from_user.id, "Сделать заказ или доставить",
                                    reply_markup=InlineKeyboardMarkup()
                                    .add(InlineKeyboardMarkup(text="Открыть карту", web_app=WebAppInfo(url=url)))
                                    )

    async def _profile_handler(self, message: types.Message, state: FSMContext):
        user = await User.objects.filter(tg_id=message.from_user.id).afirst()
        msg = "⭐️ Вашы отзывы\n"
        pr = PartnerReview.objects.filter(user=user)
        cr = CustomerReview.objects.filter(user=user)
        if pr:
            msg += f"Партнер: {pr.aggregate(Avg('points'))['points__avg']:.2f}\n"
        if cr:
            msg += f"Заказчик: {cr.aggregate(Avg('points'))['points__avg']:.2f}\n"
        if not cr and not pr:
            msg += "Отзывов пока нет 😔\n"
        msg += '\n*Статистика обновится после повторного нажатия на <b>Профиль</b>'
        await self.bot.send_message(message.from_user.id, msg,
                                    reply_markup=InlineKeyboardMarkup()
                                    .add(
                                        InlineKeyboardMarkup(text="Открыть карту",
                                                             web_app=WebAppInfo(url=url)
                                                             )
                                    ),
                                    parse_mode='HTML'
                                    )
        await state.finish()

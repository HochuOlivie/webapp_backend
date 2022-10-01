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
from django.db.models import Sum


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
        self.dp.register_message_handler(self._name_handler, state=States.name)

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
        msg = 'Теперь напишите, как к вам могут обращаться другие пользователи'
        phone = message.contact.phone_number
        await state.update_data(phone=phone)
        await self.bot.send_message(message.from_user.id, msg)
        await States.name.set()

    async def _name_handler(self, message: types.Message, state: FSMContext):
        msg = 'Теперь вы можете кликнуть на свой <b>Профиль</b>, ' \
              'открыть карту и сделать заказ или предложение на доставку из любого места в своем городе'
        name = message.text
        await state.update_data(name=name)
        User.objects.create(
            tg_id=message.from_user.id,
            tg_username=message.from_user.username,
            name=await state.get_data('name'),
            phone=await state.get_data('phone'),
        )
        await self.bot.send_message(message.from_user.id, msg,
                                    reply_markup=ReplyKeyboardMarkup().add(
                                        KeyboardButton("🗺 Профиль")
                                    ),
                                    parse_mode='HTML'
                                    )

    async def _profile_handler(self, message: types.Message, state: FSMContext):
        user = await User.objects.filter(tg_id=message.from_user.id).afirst()
        msg = f"Ваше имя: {user.name}\n\n"
        msg += "⭐️ Отзывы\n"
        pr = PartnerReview.objects.filter(user=user)
        cr = CustomerReview.objects.filter(user=user)
        if pr:
            msg += f"Партнер: {pr.agregate(Sum('points')) / pr.count():.2f}/5\n"
        if cr:
            msg += f"Курьер: {cr.agregate(Sum('points')) / cr.count():.2f}/5\n"
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

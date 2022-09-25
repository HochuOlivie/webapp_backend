from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.types import InlineKeyboardMarkup, WebAppInfo

from initialize import url
from . import keyboards
from . import callback_consts as cbc
from aiogram.dispatcher import FSMContext
from .state import States


class Registration:
    def __init__(self, bot, dp):
        self.bot: Bot = bot
        self.dp: Dispatcher = dp

    def register_commands(self):
        ...
        self.dp.register_message_handler(self._start_handler, commands=["start"], state="*")

    def register_handlers(self):
        ...
        self.dp.register_message_handler(self._contact_handler, content_types=['contact'], state='*')
        self.dp.register_message_handler(self._name_handler, state=States.name)
        # self.dp.register_callback_query_handler(self._contact_handler, text=cbc.phone, state="*")

    async def _start_handler(self, message: types.Message):
        msg = '''Привет 👋
Это бот для заказа продуктов из любых магазинов, где каждый может выступать как в роли курьера, так и в роли заказчика.
Для продолжения необходимо пройти короткую регистрацию. Нажми кнопку, чтобы поделиться номером телефона'''
        phone_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        phone_button = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
        phone_keyboard.add(phone_button)

        await self.bot.send_message(message.from_user.id, msg, reply_markup=phone_keyboard)

    async def _contact_handler(self, message: types.Message, state: FSMContext):
        msg = 'Отлично! Теперь напиши, как к тебе могут обращаться другие пользователи'
        phone = message.contact.phone_number
        await state.update_data(phone=phone)
        await self.bot.send_message(message.from_user.id, msg)
        await States.name.set()

    async def _name_handler(self, message: types.Message, state: FSMContext):
        msg = 'Теперь ты можешь открыть карту, нажав на кнопку снизу'
        name = message.text
        await state.update_data(name=name)
        await self.bot.send_message(message.from_user.id, msg,
                               reply_markup=InlineKeyboardMarkup()
                               .add(
                                   InlineKeyboardMarkup(text="Открыть карту",
                                                        web_app=WebAppInfo(url=url)
                                                        )
                               )
                               )
        await state.finish()







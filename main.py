import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import MenuButtonWebApp, ReplyKeyboardMarkup, KeyboardButton
from aiogram import types
from aiogram.utils.web_app import safe_parse_webapp_init_data
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

API_TOKEN = '5540532207:AAEB8PbJymDWQEUPJ4ZMIXkOg7K0kOHU1fc'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@dp.message_handler(commands="start")
async def on_startup(msg):
    # await bot.set_chat_menu_button(msg.from_user.id, None)
    await bot.send_message(msg.from_user.id, 'Сделайте заказ',
        reply_markup=ReplyKeyboardMarkup().add(KeyboardButton(text="Открыть карту", web_app=WebAppInfo(url=f"https://frolicking-treacle-60b728.netlify.app")))
    )

val_data = '''query_id=AAFcTsEYAAAAAFxOwRgh6M6I&user=%7B%22id%22%3A415321692%2C%22first_name%22%3A%22%F0%9F%98%B4%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22teaeye%22%2C%22language_code%22%3A%22ru%22%2C%22is_premium%22%3Atrue%7D&auth_date=1662497333&hash=619131e263c874408569a7b9dcaf643e8a277869f87fc0f788873f4fb6c652fd'''
# {"query_id":"AAFcTsEYAAAAAFxOwRgh6M6I","user":{"id":415321692,"first_name":"😴","last_name":"","username":"teaeye","language_code":"ru","is_premium":true},"auth_date":"1662497333","hash":"619131e263c874408569a7b9dcaf643e8a277869f87fc0f788873f4fb6c652fd"}

@dp.message_handler(content_types=types.ContentTypes.WEB_APP_DATA)
async def on_startup(msg: types.Message):
    # import re
    # data = msg.web_app_data.data
    # print(data)
    # data = re.split(r'|', data)
    m = f'Ищем курьеров...'
    await bot.send_message(msg.from_user.id, m)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(dp.start_polling())


# if __name__ == '__main__':
    # executor.start_polling(dp, skip_updates=True)

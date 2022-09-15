import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from aiogram import types
import json
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from aiogram.utils.web_app import safe_parse_webapp_init_data
from serializers import Order, BaseSerializer
import logging


logging.basicConfig(filename='logs.txt', encoding='utf-8', level=logging.DEBUG)

app = FastAPI()

API_TOKEN = '5540532207:AAEB8PbJymDWQEUPJ4ZMIXkOg7K0kOHU1fc'
url = 'https://timely-griffin-7f7331.netlify.app'
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
    await bot.send_message(msg.from_user.id, 'Сделайте заказ',
                           reply_markup=ReplyKeyboardMarkup()
                           .add(
                               KeyboardButton(text="Открыть карту",
                                              web_app=WebAppInfo(url=url)
                                              )
                               )
                           )


async def get_init_data(base: BaseSerializer):
    logging.debug(base.auth)
    if base.auth is None:
        raise HTTPException(status_code=400, detail="Not authorized")
    try:
        data = safe_parse_webapp_init_data(token=API_TOKEN, init_data=base.auth, _loads=json.loads)
    except ValueError:
        raise HTTPException(status_code=400, detail="Not authorized")
    return base, data


@app.post("/order")
async def read_root(data=Depends(get_init_data)):
    order, web_init_data = data
    await bot.send_message(web_init_data['user']['id'],
                           f'Ваш заказ из <b>{order.place}</b> по адресу <b>{order.address}</b> вскоре будет доставлен',
                           parse_mode='HTML')
    return {"ok": True}


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(dp.start_polling(limit=0))

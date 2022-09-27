import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django

django.setup()

import asyncio
from aiogram import Bot, Dispatcher, executor, types
import json
from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from aiogram.utils.web_app import safe_parse_webapp_init_data
from serializers import Order
import logging
from telegram.bot import DeliveryBot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db.models import Offer, User


# logging.basicConfig(filename='logs.txt', level=logging.DEBUG)

app = FastAPI()

API_TOKEN = '5506739202:AAEj9v8SPTb_faW9kJKsJGudTQlt51EUfX0'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
my_bot = DeliveryBot(bot, dp)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @dp.message_handler(commands="start")
# async def on_startup(msg):
#     await bot.send_message(msg.from_user.id, 'Сделайте заказ',
#                            reply_markup=InlineKeyboardMarkup()
#                            .add(
#                                InlineKeyboardMarkup(text="Открыть карту",
#                                               web_app=WebAppInfo(url=url)
#                                               )
#                                )
#                            )


async def get_init_data(auth: str = Header()):
    logging.debug(auth)
    if auth is None:
        raise HTTPException(status_code=400, detail="Not authorized")
    try:
        data = safe_parse_webapp_init_data(token=API_TOKEN, init_data=auth, _loads=json.loads)
    except ValueError:
        raise HTTPException(status_code=400, detail="Not authorized")
    return data


@app.post("/order")
async def make_order(order: Order, web_init_data=Depends(get_init_data)):
    await bot.send_message(web_init_data['user']['id'],
                           f'Ваш заказ из <b>{order.place}</b> по адресу <b>{order.address}</b> вскоре будет доставлен',
                           parse_mode='HTML')
    return {"ok": True}


@app.post("/offer")
async def make_offer(request: Request, web_init_data=Depends(get_init_data)):
    data = await request.json()

    coords = data['geometry']['coordinates']
    street = data['properties']['description']
    name = data['properties']['name']
    user = User.objects.filter(tg_id=web_init_data['user']['id']).first()
    if user is None:
        raise HTTPException(status_code=400, detail="Not authorized")
    else:
        Offer.objects.create(json.dumps(data), user)
    await bot.send_message(web_init_data['user']['id'],
                           'Теперь вы в роли партнера доставляете заказчикам продукты'
                           f'📍 Место <b>{name}</b>\n'
                           f'🏢 Адрес <b>{street}</b>.\n\n'
                           f'Заказчики будут высвечиваться в текущем чате',
                           parse_mode='HTML')
    return {"ok": True}


@app.get("/offers")
async def get_offers(request: Request, web_init_data=Depends(get_init_data)):
    res = [[i.feature_from, i.user.tg_id] for i in Offer.objects.all()]
    return {"ok": True, 'offers': res}


@app.on_event("startup")
async def startup_event():
    # asyncio.create_task(my_bot.start())
    ...
# executor.start_polling(dp, skip_updates=True)
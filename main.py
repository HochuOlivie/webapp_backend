import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import django
django.setup()

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from aiogram import Bot, Dispatcher, executor, types
import json
from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from aiogram.utils.web_app import safe_parse_webapp_init_data
import logging
from telegram.bot import DeliveryBot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db.models import Offer, User, Order
from asgiref.sync import sync_to_async


logging.basicConfig(filename='logs.txt', level=logging.DEBUG)

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


async def get_init_data(auth: str = Header()):
    logging.debug(auth)
    if auth is None:
        raise HTTPException(status_code=400, detail="Not authorized")
    try:
        data = safe_parse_webapp_init_data(token=API_TOKEN, init_data=auth, _loads=json.loads)
    except ValueError:
        raise HTTPException(status_code=400, detail="Not authorized")
    return data


async def delete_order_on_timeout(message: types.Message, order):
    Bot.set_current(bot)
    await asyncio.sleep(60 * 60)
    await message.edit_text("Заказ был автоматически удален по истечению срока давности")
    await sync_to_async(order.delete)()


async def delete_offer_on_timeout(message: types.Message, offer):
    Bot.set_current(bot)
    await asyncio.sleep(60 * 60)
    await message.edit_text("Предложение было автоматически удалено по истечению срока давности")

    await sync_to_async(offer.delete)()


# @app.post("/order")
async def make_order(request: Request, web_init_data=Depends(get_init_data)):
    data = await request.json()
    user = await User.objects.filter(tg_id=web_init_data['user']['id']).afirst()
    if user is None:
        raise HTTPException(status_code=400, detail="Not authorized")
    else:
        order = await sync_to_async(Order.objects.create)(feature_from=data, user=user)
    street = data['properties']['description']
    name = data['properties']['name']
    m = await bot.send_message(user.tg_id,
                           f'📦 Ждём, пока кто-нибудь из партнеров примет заказ\n\n'
                           f'📍 Место <b>{name}</b>\n'
                           f'🏢 Адрес <b>{street}</b>\n\n'
                           f'Партнер, который примет заказ, появится в текущем чате\n\n'
                           f'Заказ будет автоматически удалён через 1 час',
                           reply_markup=InlineKeyboardMarkup().add(
                               InlineKeyboardButton("❌ Отменить заказ", callback_data=f'order_delete:{order.id}')
                           ),
                           parse_mode='HTML')
    asyncio.create_task(delete_order_on_timeout(m, order))

    offers = Offer.objects.filter(feature_from__geometry__coordinates=data['geometry']['coordinates'])
    async for offer in offers:
        m = await bot.send_message(offer.user.tg_id,
                               f'Поступил заказ',
                               reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                   InlineKeyboardButton("✅ Принять", callback_data=f'order_accept:{order.id}'),
                                   InlineKeyboardButton("❌ Отклонить", callback_data=f'order_decline:{order.id}')
                               ),
                               parse_mode='HTML')
    return {"ok": True}


@app.post("/order")
async def make_order_new(request: Request, web_init_data=Depends(get_init_data)):
    data = await request.json()
    street = data['properties']['description']
    name = data['properties']['name']

    user = await User.objects.filter(tg_id=web_init_data['user']['id']).afirst()
    if user is None:
        raise HTTPException(status_code=400, detail="Not authorized")
    m = await bot.send_message(user.tg_id, f'📦 Ваш заказ'
                                           f'📍 Место <b>{name}</b>\n'
                                           f'🏢 Адрес <b>{street}</b>\n\n'
                                           f'Выберите, куда будет осуществлена доставка',
                                            reply_markup=InlineKeyboardMarkup().add(
                                                InlineKeyboardButton("➕ Добавить адрес",
                                                                     switch_inline_query_current_chat='Магнитогорск',
                                                                     callback_data=f'new_address')
                                            )
                              )


@app.post("/offer")
async def make_offer(request: Request, web_init_data=Depends(get_init_data)):
    data = await request.json()

    coords = data['geometry']['coordinates']
    street = data['properties']['description']
    name = data['properties']['name']
    user = await User.objects.filter(tg_id=web_init_data['user']['id']).afirst()
    logging.debug(user)
    logging.debug(web_init_data['user']['id'])
    if user is None:
        raise HTTPException(status_code=400, detail="Not authorized")
    else:
        offer = await sync_to_async(Offer.objects.create)(feature_from=data, user=user)
    m = await bot.send_message(web_init_data['user']['id'],
                           '🚴 Теперь вы в роли партнера доставляете заказчикам продукты\n\n'
                           f'📍 Место <b>{name}</b>\n'
                           f'🏢 Адрес <b>{street}</b>.\n\n'
                           f'Заказчики будут высвечиваться в текущем чате\n\n'
                           f'Предложение будет автоматически удалено через 1 час',
                           reply_markup=InlineKeyboardMarkup().add(
                               InlineKeyboardButton("❌ Больше не принимать заказы", callback_data=f'offer_delete:{offer.id}')
                           ),
                           parse_mode='HTML')
    asyncio.create_task(delete_offer_on_timeout(m, offer))

    orders = Order.objects.filter(feature_from__geometry__coordinates=data['geometry']['coordinates'])
    async for order in orders:
        await bot.send_message(web_init_data["user"]["id"],
                               f'Поступил заказ',
                               reply_markup=InlineKeyboardMarkup(row_width=2).add(
                                   InlineKeyboardButton("✅ Принять", callback_data=f'order_accept:{order.id}'),
                                   InlineKeyboardButton("❌ Отклонить", callback_data=f'order_decline:{order.id}')
                               ),
                               parse_mode='HTML')
    return {"ok": True}


@app.get("/offers")
async def get_offers(request: Request, web_init_data=Depends(get_init_data)):
    res = [i.feature_from async for i in Offer.objects.all()]
    return {"ok": True, 'features': res}


@app.get("/orders")
async def get_offers(request: Request, web_init_data=Depends(get_init_data)):
    res = [i.feature_from async for i in Order.objects.all()]
    return {"ok": True, 'features': res}


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(my_bot.start())
    # ...

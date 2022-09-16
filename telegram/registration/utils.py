# import decorator
# from aiogram import types
# from aiogram.dispatcher import FSMContext
# from typing import Union
# from aiogram.methods import DeleteMessage
#
#
# @decorator.decorator
# async def deletable_messages(coro, message: Union[types.message, types.CallbackQuery], context: FSMContext, *args, **kwargs):
#     res = await coro(message, context, *args, **kwargs)
#     await context.set_data(delete_messages=res['message_id'])
#

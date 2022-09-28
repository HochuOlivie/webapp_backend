from aiogram import executor, Bot, Dispatcher
from .registration.branches import Registration
from .main.branches import Main

BRANCHES = [Registration, Main]


class DeliveryBot:
    def __init__(self, bot: Bot, dp: Dispatcher):
        self.bot = bot
        self.dp = dp
        branches_list = []
        for branch in BRANCHES:
            b = branch(self.bot, self.dp)
            branches_list.append(b)
            b.register_commands()
        for b in branches_list:
            b.register_handlers()

    async def start(self):
        if not self.dp.is_polling():
            await self.dp.skip_updates()
            await self.dp.start_polling()

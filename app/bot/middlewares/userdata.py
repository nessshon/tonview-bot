from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import User
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from pytonapi import AsyncTonapi

from app.db.database import Database


class UserDataMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ['error', 'update']

    async def pre_process(self, obj, data, *args):
        dp: Dispatcher = Dispatcher.get_current()
        bot: Bot = Bot.get_current()
        db: Database = bot.get("db")

        from ...config import Config
        config: Config = bot.get("config")

        user: User = User.get_current()
        state: FSMContext = FSMContext(dp.storage, user.id, user.id)

        user_data = await state.get_data()
        testnet = user_data.get("testnet", False)
        tonapi_key = user_data.get("tonapi_key", config.tonapi.KEY)
        tonapi = AsyncTonapi(tonapi_key, testnet=testnet, max_retries=10)
        message_id = user_data.get("message_id", None)

        data["message_id"] = message_id
        data["chat_id"] = user.id
        data["tonapi"] = tonapi
        data["bot"] = bot
        data["db"] = db

import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import (Message, BotCommand,
                           BotCommandScopeAllPrivateChats)

from app.bot.filters import IsPrivate
from app.bot.handlers import windows
from app.bot.keyboards import inline
from app.bot.middlewares.throttling import rate_limit
from app.bot.states import State
from app.bot.texts import messages
from app.bot.utils.message import (edit_or_send_message,
                                   delete_previous_message, delete_message)
from app.db.database import Database
from app.db.models import User


@rate_limit(2)
async def start(message: Message, state: FSMContext, db: Database, chat_id: int) -> None:
    msg = await message.answer(text="👋")
    await delete_previous_message(message.bot, state)
    async with state.proxy() as data: data.clear()  # noqa:E701
    await state.update_data(message_id=msg.message_id)

    if not await User.is_exist(db.sessionmaker, user_id=chat_id): await User.add(  # noqa:E701
        sessionmaker=db.sessionmaker,
        user_id=chat_id,
        name=message.from_user.full_name,
    )

    await asyncio.sleep(1.5)
    await windows.main(
        bot=message.bot, state=state,
        chat_id=chat_id, message_id=msg.message_id,
    )
    await delete_message(message)


@rate_limit(1)
async def set_api_key(message: Message, state: FSMContext, chat_id: int, message_id: int) -> None:
    await windows.set_api_key(
        bot=message.bot, state=state,
        chat_id=chat_id, message_id=message_id,
    )
    await delete_message(message)


@rate_limit(1)
async def switch_network(message: Message, state: FSMContext, chat_id: int, message_id: int) -> None:
    data = await state.get_data()
    testnet = data.get("testnet", False)
    await state.update_data(testnet=False if testnet else True)

    text = messages.switched_to_mainnet if testnet else messages.switched_to_testnet
    markup = inline.go_main()

    await edit_or_send_message(
        bot=message.bot, state=state,
        chat_id=chat_id, message_id=message_id,
        text=text, markup=markup,
    )
    await State.main.set()
    await delete_message(message)


def register(dp: Dispatcher) -> None:
    dp.register_message_handler(
        start, IsPrivate(),
        commands="start", state="*",
    )
    dp.register_message_handler(
        set_api_key, IsPrivate(),
        commands="set_api_key", state="*",
    )
    dp.register_message_handler(
        switch_network, IsPrivate(),
        commands="switch_network", state="*",
    )


async def setup(dp: Dispatcher) -> None:
    commands = [
        BotCommand("/start", "Restart bot"),
        BotCommand("/set_api_key", "Set your API key"),
        BotCommand("/switch_network", "Switch network mode"),
    ]
    await dp.bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats(),
    )


async def delete(dp: Dispatcher):
    await dp.bot.delete_my_commands(
        scope=BotCommandScopeAllPrivateChats(),
    )

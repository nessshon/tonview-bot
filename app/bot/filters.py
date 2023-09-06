from aiogram import Dispatcher
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery, ChatType


class IsPrivate(BoundFilter):

    async def check(self, update: Message | CallbackQuery) -> bool:
        chat = update.chat if isinstance(update, Message) else update.message.chat
        return ChatType.PRIVATE == chat.type


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsPrivate)

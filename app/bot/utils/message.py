from contextlib import suppress

from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.utils.exceptions import (MessageCantBeDeleted, MessageToDeleteNotFound,
                                      MessageToEditNotFound, MessageCantBeEdited, MessageNotModified)


async def delete_message(message: Message) -> None:
    """
    Deletes the given Telegram message.

    :param message: The :class:`Message` to be deleted.
    :return: None
    """
    with suppress(MessageToDeleteNotFound, MessageCantBeDeleted):
        await message.delete()


async def delete_previous_message(bot: Bot, state: FSMContext) -> None:
    """
    Deletes the previous Telegram message.

    :param bot: The :class:`Bot` instance used to delete the message.
    :param state: The :class:`FSMContext` instance representing
        the current state of the conversation.
    :return: None
    """
    data = await state.get_data()

    with suppress(KeyError, MessageToDeleteNotFound, MessageCantBeDeleted):
        await bot.delete_message(
            chat_id=state.chat, message_id=data["message_id"]
        )


async def edit_or_send_message(bot: Bot, state: FSMContext,
                               chat_id: int, message_id: int, text: str,
                               markup: InlineKeyboardMarkup = None,
                               ) -> Message | None:
    try:
        message = await bot.edit_message_text(
            text=text, chat_id=chat_id,
            message_id=message_id, reply_markup=markup,
        )

    except (MessageToEditNotFound, MessageCantBeEdited, MessageNotModified):
        message = await bot.send_message(
            chat_id=chat_id, text=text, reply_markup=markup
        )
        await delete_previous_message(bot=bot, state=state)
        await state.update_data(message_id=message.message_id)

    return message

from contextlib import suppress

from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup
from aiogram.utils.exceptions import (MessageCantBeDeleted, MessageToDeleteNotFound,
                                      MessageToEditNotFound, MessageCantBeEdited, MessageNotModified, BadRequest)


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
    """
    Edit or send a message using the Telegram Bot API.

    :param bot: The Bot instance used to send or edit the message.
    :param state: The FSMContext instance.
    :param chat_id: The ID of the chat where the message will be sent or edited.
    :param message_id: The ID of the message to be edited.
    :param text: The text of the message.
    :param markup: The inline keyboard markup for the message (default: None).
    :return: Message | None: The edited or sent message, or None if an error occurred.
    """
    try:
        message = await bot.edit_message_text(
            text=text, chat_id=chat_id,
            message_id=message_id, reply_markup=markup,
        )

    except (MessageToEditNotFound, MessageCantBeEdited, MessageNotModified, BadRequest):
        message = await bot.send_message(
            chat_id=chat_id, text=text, reply_markup=markup
        )
        await delete_previous_message(bot=bot, state=state)
        await state.update_data(message_id=message.message_id)

    return message

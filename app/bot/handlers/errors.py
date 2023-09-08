import json
import logging
from contextlib import suppress

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Update, User
from aiogram.utils.exceptions import (BotBlocked, ChatNotFound, InvalidQueryID,
                                      MessageToEditNotFound, MessageCantBeEdited, MessageNotModified,
                                      MessageToDeleteNotFound, MessageCantBeDeleted, MessageIsTooLong)
from aiogram.utils.markdown import hcode, hbold
from pytonapi.exceptions import TONAPIUnauthorizedError, TONAPITooManyRequestsError

from . import windows
from ..utils.message import delete_message
from ...config import Config


async def error_handler(update: Update, exception: Exception) -> bool:
    """
    Exceptions handler. Catches all exceptions within task factory tasks

    :param update:
    :param exception:
    :return: stdout logging
    """

    if isinstance(exception, TONAPIUnauthorizedError):
        user: User = User.get_current()
        dp: Dispatcher = Dispatcher.get_current()
        state = FSMContext(dp.storage, user.id, user.id)

        data = await state.get_data()
        message_id = data.get("message_id", None)

        await windows.invalid_api_key(
            bot=dp.bot, state=state,
            chat_id=user.id, message_id=message_id,
        )
        await delete_message(update.message)

        return True

    if isinstance(exception, TONAPITooManyRequestsError):
        user: User = User.get_current()
        dp: Dispatcher = Dispatcher.get_current()
        state = FSMContext(dp.storage, user.id, user.id)

        data = await state.get_data()
        message_id = data.get("message_id", None)

        await windows.too_many_requests(
            bot=dp.bot, state=state,
            chat_id=user.id, message_id=message_id,
        )
        await delete_message(update.message)

        return True

    if isinstance(exception, ChatNotFound):
        logging.exception(f'ChatNotFound: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, BotBlocked):
        logging.exception(f'BotBlocked: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, InvalidQueryID):
        logging.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, MessageIsTooLong):
        logging.exception(f'MessageIsTooLong: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logging.exception(f'MessageToDeleteNotFound: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, MessageCantBeDeleted):
        logging.exception(f'MessageCantBeDeleted: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, MessageToEditNotFound):
        logging.exception(f'MessageToEditNotFound: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, MessageCantBeEdited):
        logging.exception(f'MessageCantBeEdited: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, MessageNotModified):
        logging.exception(f'MessageNotModified: {exception} \nUpdate: {update}')
        return True

    config: Config = update.bot.get("config")
    with suppress(ChatNotFound, BotBlocked):
        text = (
            "#ERROR\n\n"
            "<b>Update:</b>\n"
            "{update}\n\n"
            "<b>Exception:</b>\n"
            "{exception}"
        )
        update_json = json.dumps(
            json.loads(update.as_json()),
            ensure_ascii=False,
            sort_keys=True,
            indent=1,
        )
        await update.bot.send_message(
            chat_id=config.bot.DEV_ID,
            text=text.format(
                update=hcode(update_json),
                exception=hbold(exception),
            )
        )

    logging.exception(f'Update: {update} \n{exception}')
    return True


def register(dp: Dispatcher) -> None:
    dp.register_errors_handler(error_handler)

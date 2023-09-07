from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageIsTooLong

from app.bot.filters import IsPrivate
from app.bot.handlers import windows
from app.bot.keyboards import callback_data
from app.bot.states import State
from app.bot.texts import messages


async def main(call: CallbackQuery, state: FSMContext, chat_id, message_id) -> None:
    match call.data:
        case callback_data.go_main:
            await windows.main(
                bot=call.bot, state=state,
                chat_id=chat_id, message_id=message_id,
            )
        case cdata if cdata in [callback_data.switch_to_mainnet, callback_data.switch_to_testnet]:
            testnet = True if cdata == callback_data.switch_to_testnet else False
            text = messages.call__switched_to_testnet if testnet else messages.call__switched_to_mainnet
            await call.answer(text, show_alert=True)
            await state.update_data(testnet=testnet)
            await windows.main(
                bot=call.bot, state=state,
                chat_id=chat_id, message_id=message_id
            )
        case callback_data.set_api_key:
            await windows.set_api_key(
                bot=call.bot, state=state,
                chat_id=chat_id, message_id=message_id
            )
        case callback_data.del_api_key:
            async with state.proxy() as data:
                data.pop("tonapi_key")
            text = messages.call__api_key_removed
            await call.answer(text, show_alert=True)
            await windows.main(
                bot=call.bot, state=state,
                chat_id=chat_id, message_id=message_id,
            )

    await call.answer()


async def set_api_key(call: CallbackQuery, state: FSMContext, chat_id, message_id) -> None:
    match call.data:
        case callback_data.back:
            await windows.main(
                bot=call.bot, state=state,
                chat_id=chat_id, message_id=message_id
            )

    await call.answer()


async def contract(call: CallbackQuery, state: FSMContext, chat_id, message_id) -> None:
    match call.data:
        case callback_data.go_main:
            await windows.main(
                bot=call.bot, state=state,
                chat_id=chat_id, message_id=message_id,
            )
        case callback_data.attributes:
            try:
                await windows.detail_attributes(
                    bot=call.bot, state=state,
                    chat_id=chat_id, message_id=message_id
                )
            except KeyError:
                text = messages.call__attributes_not_found
                await call.answer(text, show_alert=True)
        case callback_data.metadata:
            await windows.detail_metadata(
                bot=call.bot, state=state,
                chat_id=chat_id, message_id=message_id
            )
        case callback_data.show_json:
            try:
                await windows.detail_json(
                    bot=call.bot, state=state,
                    chat_id=chat_id, message_id=message_id,
                )
            except MessageIsTooLong:
                text = messages.call__json_too_long
                await call.answer(text, show_alert=True)

    await call.answer()


async def details(call: CallbackQuery, state: FSMContext, chat_id, message_id) -> None:
    data = await state.get_data()

    match call.data:
        case callback_data.back:
            match data["contract_type"]:
                case "jetton":
                    await windows.information_jetton(
                        bot=call.bot, state=state,
                        chat_id=chat_id, message_id=message_id
                    )
                case "nft":
                    await windows.information_nft(
                        bot=call.bot, state=state,
                        chat_id=chat_id, message_id=message_id
                    )
                case "collection":
                    await windows.information_collection(
                        bot=call.bot, state=state,
                        chat_id=chat_id, message_id=message_id
                    )
                case "account":
                    await windows.information(
                        bot=call.bot, state=state,
                        chat_id=chat_id, message_id=message_id
                    )

    await call.answer()


def register(dp: Dispatcher) -> None:
    dp.register_callback_query_handler(
        set_api_key, IsPrivate(),
        state=State.set_api_key,
    )
    dp.register_callback_query_handler(
        contract, IsPrivate(),
        state=State.information,
    )
    dp.register_callback_query_handler(
        details, IsPrivate(),
        state=State.detail,
    )
    dp.register_callback_query_handler(
        main, IsPrivate(),
        state="*",
    )

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from pytonapi import AsyncTonapi
from pytonapi.exceptions import TONAPIUnauthorizedError, TONAPITooManyRequestsError

from app.bot.filters import IsPrivate
from app.bot.handlers import windows
from app.bot.keyboards import inline
from app.bot.middlewares.throttling import ThrottlingContext, EMOJIS_MAGNIFIER, rate_limit
from app.bot.states import State
from app.bot.texts import messages
from app.bot.utils.crypto import encrypt_key
from app.bot.utils.message import delete_message, edit_or_send_message
from app.config import Config


@rate_limit(2)
async def main(message: Message, state: FSMContext, tonapi: AsyncTonapi, chat_id, message_id):
    if message.text:
        try:
            async with ThrottlingContext(bot=message.bot, state=state,
                                         chat_id=chat_id, message_id=message_id,
                                         emojis=EMOJIS_MAGNIFIER):
                match message.text:
                    case domain if domain[-4:] == ".ton" or domain[-5:] == ".t.me":
                        request = await tonapi.dns.resolve(domain.lower())
                        account_id = request.wallet.address.to_userfriendly()
                    case address if len(address) == 48 or len(address) == 66:
                        account_id = address
                    case _:
                        account_id = None

                if account_id:
                    account = await tonapi.accounts.get_info(account_id)

                    match account.interfaces:
                        case None:
                            await state.update_data(
                                contract_type="account",
                                account=account.dict(),
                            )
                            await windows.information(
                                bot=message.bot, state=state,
                                chat_id=chat_id, message_id=message_id,
                            )
                        case interfaces if "tep74" in interfaces:
                            jetton = await tonapi.jettons.get_info(account_id)
                            await state.update_data(
                                contract_type="jetton",
                                account=account.dict(), jetton=jetton.dict(),
                            )
                            await windows.information_jetton(
                                bot=message.bot, state=state,
                                chat_id=chat_id, message_id=message_id,
                            )

                        case interfaces if "tep62_item" in interfaces:
                            nft = await tonapi.nft.get_item_by_address(account_id)
                            await state.update_data(
                                contract_type="nft",
                                account=account.dict(), nft=nft.dict(),
                            )
                            await windows.information_nft(
                                bot=message.bot, state=state,
                                chat_id=chat_id, message_id=message_id,
                            )
                        case interfaces if "tep62_collection" in interfaces:
                            collection = await tonapi.nft.get_collection_by_collection_address(account_id)
                            await state.update_data(
                                contract_type="collection",
                                account=account.dict(), collection=collection.dict(),
                            )
                            await windows.information_collection(
                                bot=message.bot, state=state,
                                chat_id=chat_id, message_id=message_id,
                            )
                        case _:
                            await state.update_data(
                                contract_type="account",
                                account=account.dict(),
                            )
                            await windows.information(
                                bot=message.bot, state=state,
                                chat_id=chat_id, message_id=message_id,
                            )
                else:
                    event = await tonapi.events.get_event(event_id=message.text)
                    await state.update_data(from_pages=False, event=event.dict())
                    await windows.information_event(
                        bot=message.bot, state=state,
                        chat_id=chat_id, message_id=message_id,
                    )

        except (TONAPIUnauthorizedError, TONAPITooManyRequestsError):
            raise

        except Exception as e:
            text = messages.not_found
            markup = inline.go_main()
            await edit_or_send_message(
                bot=message.bot, state=state,
                chat_id=chat_id, message_id=message_id,
                text=text, markup=markup,
            )
            await delete_message(message)
            await State.main.set()

            if "encoding/hex" in str(e):
                pass
            else:
                raise

    await delete_message(message)


@rate_limit(1)
async def set_api_key(message: Message, state: FSMContext, chat_id, message_id):
    if message.text:
        try:
            config: Config = message.bot.get("config")

            async with ThrottlingContext(bot=message.bot, state=state,
                                         chat_id=chat_id, message_id=message_id):
                tonapi = AsyncTonapi(message.text)
                await tonapi.rates.get_prices(["TON"], ["USD"])

                tonapi_key = encrypt_key(config.tonapi.ENCRYPTION_KEY, message.text)
                await state.update_data(tonapi_key=tonapi_key.decode())

                await windows.main(
                    bot=message.bot, state=state,
                    chat_id=chat_id, message_id=message_id,
                )

        except TONAPIUnauthorizedError:
            text = messages.api_key_invalid__input
            markup = inline.back()
            await edit_or_send_message(
                bot=message.bot, state=state,
                chat_id=chat_id, message_id=message_id,
                text=text, markup=markup
            )

    await delete_message(message)


async def invalid_api_key(message: Message, state: FSMContext, chat_id, message_id):
    if message.text:
        try:
            config: Config = message.bot.get("config")

            async with ThrottlingContext(bot=message.bot, state=state,
                                         chat_id=chat_id, message_id=message_id):
                tonapi = AsyncTonapi(message.text)
                await tonapi.rates.get_prices(tokens=["TON"], currencies=["USD"])

                tonapi_key = encrypt_key(config.tonapi.ENCRYPTION_KEY, message.text)
                await state.update_data(tonapi_key=tonapi_key.decode())

                await windows.main(
                    bot=message.bot, state=state,
                    chat_id=chat_id, message_id=message_id,
                )

        except TONAPIUnauthorizedError:
            text = messages.api_key_invalid__error
            markup = inline.api_key_invalid()
            await edit_or_send_message(
                bot=message.bot, state=state,
                chat_id=chat_id, message_id=message_id,
                text=text, markup=markup
            )

    await delete_message(message)


def register(dp: Dispatcher) -> None:
    dp.register_message_handler(
        set_api_key, IsPrivate(),
        state=State.set_api_key, content_types="any",
    )
    dp.register_message_handler(
        main, IsPrivate(),
        state="*", content_types="any",
    )

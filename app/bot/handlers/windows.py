import json

from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold, hcode
from pytonapi.schema.accounts import Account
from pytonapi.schema.blockchain import Transaction
from pytonapi.schema.jettons import JettonInfo
from pytonapi.schema.nft import NftItem, NftCollection

from app.bot.keyboards import inline
from app.bot.states import State
from app.bot.texts import messages
from app.bot.utils.message import edit_or_send_message


async def main(bot: Bot, state: FSMContext, chat_id: int, message_id: int) -> None:
    data = await state.get_data()

    text = messages.main
    markup = inline.main(data.get("testnet", False), "tonapi_key" in data)

    await edit_or_send_message(
        bot=bot, state=state,
        text=text, markup=markup,
        chat_id=chat_id, message_id=message_id,
    )
    await State.main.set()


async def set_api_key(bot: Bot, state: FSMContext, chat_id: int, message_id: int) -> None:
    text = messages.set_api_key
    markup = inline.back()

    await edit_or_send_message(
        bot=bot, state=state,
        text=text, markup=markup,
        chat_id=chat_id, message_id=message_id,
    )
    await State.set_api_key.set()


async def invalid_api_key(bot: Bot, state: FSMContext, chat_id: int, message_id: int) -> None:
    text = messages.api_key_invalid__error
    markup = inline.api_key_invalid()

    await edit_or_send_message(
        bot=bot, state=state,
        chat_id=chat_id, message_id=message_id,
        text=text, markup=markup,
    )
    await State.api_key_invalid.set()


async def too_many_requests(bot: Bot, state: FSMContext, chat_id: int, message_id: int) -> None:
    text = messages.too_many_requests__error
    markup = inline.set_api_key()

    await edit_or_send_message(
        bot=bot, state=state,
        chat_id=chat_id, message_id=message_id,
        text=text, markup=markup,
    )
    await State.main.set()


async def information(bot: Bot, state: FSMContext, chat_id: int, message_id: int) -> None:
    data = await state.get_data()

    account: Account = Account(**data["account"])
    chl = f"ton://transfer/{account.address.to_userfriendly()}"
    preview_url = f"https://chart.googleapis.com/chart?chs=512x512&cht=qr&chl={chl}"

    text = messages.information(account, preview_url)
    markup = inline.information(account.address.to_userfriendly())

    await edit_or_send_message(
        bot=bot, state=state,
        text=text, markup=markup,
        chat_id=chat_id, message_id=message_id,
    )
    await State.information.set()


async def information_jetton(bot: Bot, state: FSMContext, chat_id: int, message_id: int) -> None:
    data = await state.get_data()

    account: Account = Account(**data["account"])
    jetton: JettonInfo = JettonInfo(**data["jetton"])

    markup = inline.information_jetton(account.address.to_userfriendly())
    text = messages.information_jetton(account, jetton)

    await edit_or_send_message(
        bot=bot, state=state,
        text=text, markup=markup,
        chat_id=chat_id, message_id=message_id,
    )
    await State.information.set()


async def information_nft(bot: Bot, state: FSMContext, chat_id: int, message_id: int) -> None:
    data = await state.get_data()

    account: Account = Account(**data["account"])
    nft: NftItem = NftItem(**data["nft"])

    markup = inline.information_nft(account.address.to_userfriendly())
    text = messages.information_nft(account, nft)

    await edit_or_send_message(
        bot=bot, state=state,
        text=text, markup=markup,
        chat_id=chat_id, message_id=message_id,
    )
    await State.information.set()


async def information_collection(bot: Bot, state: FSMContext, chat_id: int, message_id: int) -> None:
    data = await state.get_data()

    account: Account = Account(**data["account"])
    collection: NftCollection = NftCollection(**data["collection"])

    markup = inline.information_collection(account.address.to_userfriendly())
    text = messages.information_collection(account, collection)

    await edit_or_send_message(
        bot=bot, state=state,
        text=text, markup=markup,
        chat_id=chat_id, message_id=message_id,
    )
    await State.information.set()


async def information_transaction(bot: Bot, state: FSMContext, chat_id: int, message_id: int) -> None:
    data = await state.get_data()

    transaction: Transaction = Transaction(**data["transaction"])

    markup = inline.information_transaction()
    text = messages.contract_transaction(transaction)

    await edit_or_send_message(
        bot=bot, state=state,
        text=text, markup=markup,
        chat_id=chat_id, message_id=message_id,
    )
    await State.information.set()


async def detail_attributes(bot: Bot, state: FSMContext, chat_id: int, message_id: int) -> None:
    data = await state.get_data()

    nft: NftItem = NftItem(**data["nft"])

    markup = inline.back()
    text = '\n\n'.join(
        [f"• {hbold(attr.get('trait_type'))}: {hcode(attr.get('value'))}"
         for attr in nft.metadata["attributes"]]
    )
    await edit_or_send_message(
        bot=bot, state=state,
        text=text, markup=markup,
        chat_id=chat_id, message_id=message_id,
    )
    await State.detail.set()


async def detail_metadata(bot: Bot, state: FSMContext, chat_id: int, message_id: int) -> None:
    data = await state.get_data()

    if data["contract_type"] == "nft":
        item: NftItem = NftItem(**data["nft"])
    elif data["contract_type"] == "jetton":
        item: JettonInfo = JettonInfo(**data["jetton"])
        item.metadata = item.metadata.dict()
    else:
        item: NftCollection = NftCollection(**data["collection"])

    text = hcode(json.dumps(item.metadata, ensure_ascii=False, sort_keys=True, indent=2))
    markup = inline.back()

    await edit_or_send_message(
        bot=bot, state=state,
        text=text, markup=markup,
        chat_id=chat_id, message_id=message_id,
    )
    await State.detail.set()


async def detail_json(bot: Bot, state: FSMContext, chat_id: int, message_id: int) -> None:
    data = await state.get_data()

    transaction: Transaction = Transaction(**data["transaction"])

    markup = inline.back()
    text = hcode(json.dumps(transaction.dict(), ensure_ascii=False, sort_keys=True, indent=2))

    await edit_or_send_message(
        bot=bot, state=state,
        text=text, markup=markup,
        chat_id=chat_id, message_id=message_id,
    )
    await State.detail.set()

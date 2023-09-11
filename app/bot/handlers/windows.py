import json
import datetime

from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hbold, hcode
from aiogram.utils.parts import paginate
from pytonapi.schema.accounts import Account
from pytonapi.schema.blockchain import Transaction
from pytonapi.schema.events import AccountEvents
from pytonapi.schema.jettons import JettonInfo
from pytonapi.schema.nft import NftItem, NftCollection

from app.bot.keyboards import inline, callback_data
from app.bot.keyboards.inline import InlineKeyboardCalendar
from app.bot.states import State
from app.bot.texts import messages, buttons
from app.bot.utils.address import AddressDisplay
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

    text = await messages.information(account, preview_url)
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
    text = await messages.information_jetton(account, jetton)

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
    text = await messages.information_nft(account, nft)

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
    text = await messages.information_collection(account, collection)

    await edit_or_send_message(
        bot=bot, state=state,
        text=text, markup=markup,
        chat_id=chat_id, message_id=message_id,
    )
    await State.information.set()


async def information_event(bot: Bot, state: FSMContext, chat_id: int, message_id: int) -> None:
    data = await state.get_data()

    event: Transaction = Transaction(**data["event"])

    markup = inline.information_event()
    text = await messages.contract_event(event)

    await edit_or_send_message(
        bot=bot, state=state,
        text=text, markup=markup,
        chat_id=chat_id, message_id=message_id,
    )
    await State.information_event.set()


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


async def information_event_json(bot: Bot, state: FSMContext, chat_id: int, message_id: int) -> None:
    data = await state.get_data()

    event: Transaction = Transaction(**data["event"])

    markup = inline.back()
    text = hcode(json.dumps(event.dict(), ensure_ascii=False, sort_keys=True, indent=2))

    await edit_or_send_message(
        bot=bot, state=state,
        text=text, markup=markup,
        chat_id=chat_id, message_id=message_id,
    )
    await State.information_event_json.set()


async def events_page(bot: Bot, state: FSMContext, chat_id: int, message_id: int) -> None:
    data = await state.get_data()

    account: Account = Account(**data["account"])
    data_items = AccountEvents(**data["events"])

    current_page, limit = data.get("page", 1), 10
    total_pages = data.get("total_pages", 2)

    items = [(buttons.create_event_button(event), event.event_id)
             for event in paginate(data_items.events, current_page - 1, limit)]
    total_pages += 1 if len(items) == limit else 0

    inline_query = f"{callback_data.events} {account.address.to_userfriendly()}"
    after_buttons = inline.export_as__csv_json().inline_keyboard
    before_buttons = inline.open_in_inline_mode__back(inline_query).inline_keyboard

    paginator = inline.InlineKeyboardPaginator(
        items=items, total_pages=total_pages, current_page=current_page,
        after_buttons=after_buttons, before_buttons=before_buttons,
    )
    text = messages.events_page.format(
        address=AddressDisplay(account).title()
    )
    markup = paginator.markup

    await edit_or_send_message(
        bot=bot, state=state,
        text=text, markup=markup,
        chat_id=chat_id, message_id=message_id,
    )
    await State.detail.set()


async def select_date(bot: Bot, state: FSMContext, chat_id: int, message_id: int) -> None:
    data = await state.get_data()

    date = data.get("date", datetime.datetime.now().timestamp())
    start_date = data.get("start_date", None)
    end_date = data.get("end_date", None)

    text = messages.select_date.format(
        start_date=datetime.datetime.fromtimestamp(start_date).strftime("%Y-%m-%d %H:%M:%S")
        if start_date else "Select start date",
        end_date=datetime.datetime.fromtimestamp(end_date).strftime("%Y-%m-%d %H:%M:%S")
        if end_date else "Select end date"
    )
    keyboard = InlineKeyboardCalendar(
        date=date,
        start_date=start_date,
        end_date=end_date,
    )

    await edit_or_send_message(
        bot=bot, state=state,
        chat_id=chat_id, message_id=message_id,
        text=text, markup=keyboard.markup(),
    )
    await State.select_date.set()


async def confirm_export(bot: Bot, state: FSMContext, chat_id: int, message_id: int) -> None:
    data = await state.get_data()

    start_date = data.get("start_date")
    end_date = data.get("end_date")
    all_time = data.get("all_time")

    if all_time == InlineKeyboardCalendar.cb_export_for_all_time:
        text = messages.confirm_export_all_time.format(
            export_type=getattr(buttons, data.get("export_type")),
            export_date=InlineKeyboardCalendar.export_for_all_time,
        )
    else:
        text = messages.confirm_export.format(
            start_date=datetime.datetime.fromtimestamp(start_date).strftime("%Y-%m-%d %H:%M")
            if start_date else "Select start date",
            end_date=datetime.datetime.fromtimestamp(end_date).strftime("%Y-%m-%d %H:%M")
            if end_date else "Select end date",
            export_type=getattr(buttons, data.get("export_type")),
        )
    markup = inline.back__confirm()

    await edit_or_send_message(
        bot=bot, state=state,
        chat_id=chat_id, message_id=message_id,
        text=text, markup=markup,
    )
    await State.confirm_export.set()

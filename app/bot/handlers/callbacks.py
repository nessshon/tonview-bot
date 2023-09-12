import asyncio
import calendar
import datetime

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageIsTooLong
from pytonapi import AsyncTonapi
from pytonapi.schema.accounts import Account
from pytonapi.schema.events import AccountEvents

from app.bot.filters import IsPrivate
from app.bot.handlers import windows
from app.bot.keyboards import callback_data, inline
from app.bot.keyboards.inline import InlineKeyboardCalendar
from app.bot.middlewares.throttling import ThrottlingContext, EMOJIS_MAGNIFIER, rate_limit
from app.bot.states import State
from app.bot.texts import messages, buttons
from app.bot.exceptions import BadRequestMessageIsTooLong
from app.bot.utils.coingecko import Coingecko
from app.bot.utils.export import ExportManager
from app.bot.utils.message import edit_or_send_message, delete_previous_message


@rate_limit(1)
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
                chat_id=chat_id, message_id=message_id,
            )
        case callback_data.set_api_key:
            await windows.set_api_key(
                bot=call.bot, state=state,
                chat_id=chat_id, message_id=message_id,
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


@rate_limit(1)
async def set_api_key(call: CallbackQuery, state: FSMContext, chat_id, message_id) -> None:
    match call.data:
        case callback_data.back:
            await windows.main(
                bot=call.bot, state=state,
                chat_id=chat_id, message_id=message_id,
            )

    await call.answer()


@rate_limit(1)
async def contract(call: CallbackQuery, state: FSMContext, tonapi: AsyncTonapi, chat_id, message_id) -> None:
    data = await state.get_data()

    match call.data:
        case callback_data.go_main:
            await windows.main(
                bot=call.bot, state=state,
                chat_id=chat_id, message_id=message_id,
            )
        case callback_data.events:
            async with ThrottlingContext(bot=call.bot, state=state,
                                         chat_id=chat_id, message_id=message_id,
                                         emojis=EMOJIS_MAGNIFIER):
                account: Account = Account(**data["account"])
                events = await tonapi.accounts.get_events(
                    account_id=account.address.to_userfriendly(), limit=10,
                )
                await state.update_data(
                    page=1, total_pages=1, events=events.dict()
                )

            await windows.events_page(
                bot=call.bot, state=state,
                chat_id=chat_id, message_id=message_id,
            )
        case callback_data.attributes:
            try:
                await windows.detail_attributes(
                    bot=call.bot, state=state,
                    chat_id=chat_id, message_id=message_id,
                )
            except KeyError:
                text = messages.call__attributes_not_found
                await call.answer(text, show_alert=True)
            except (MessageIsTooLong, BadRequestMessageIsTooLong):
                text = messages.call__attributes_too_long
                await call.answer(text, show_alert=True)

        case callback_data.metadata:
            try:
                await windows.detail_metadata(
                    bot=call.bot, state=state,
                    chat_id=chat_id, message_id=message_id,
                )
            except (MessageIsTooLong, BadRequestMessageIsTooLong):
                text = messages.call__metadata_too_long
                await call.answer(text, show_alert=True)

    await call.answer()


@rate_limit(0.5)
async def details(call: CallbackQuery, state: FSMContext, tonapi: AsyncTonapi, chat_id, message_id) -> None:
    data = await state.get_data()

    match call.data:
        case callback_data.back:
            await state.update_data(page=1, total_pages=1)

            match data["contract_type"]:
                case "jetton":
                    await windows.information_jetton(
                        bot=call.bot, state=state,
                        chat_id=chat_id, message_id=message_id,
                    )
                case "nft":
                    await windows.information_nft(
                        bot=call.bot, state=state,
                        chat_id=chat_id, message_id=message_id,
                    )
                case "collection":
                    await windows.information_collection(
                        bot=call.bot, state=state,
                        chat_id=chat_id, message_id=message_id,
                    )
                case "account":
                    await windows.information(
                        bot=call.bot, state=state,
                        chat_id=chat_id, message_id=message_id,
                    )

        case cdata if cdata in [callback_data.export_as_csv, callback_data.export_as_json]:
            if not data.get("tonapi_key", None):
                text = messages.call__need_api_key
                await call.answer(text, show_alert=True)
            else:
                await state.update_data(
                    start_date=None, end_date=None, export_type=cdata
                )
                await windows.select_date(
                    bot=call.bot, state=state,
                    chat_id=chat_id, message_id=message_id,
                )

        case event_id if len(event_id) == 64:
            async with ThrottlingContext(bot=call.bot, state=state,
                                         chat_id=chat_id, message_id=message_id,
                                         emojis=EMOJIS_MAGNIFIER):
                event = await tonapi.blockchain.get_transaction_data(
                    transaction_id=event_id
                )
                await state.update_data(from_pages=True, event=event.dict())
                await windows.information_event(
                    bot=call.bot, state=state,
                    chat_id=chat_id, message_id=message_id,
                )

        case page if call.data.startswith("page"):

            account: Account = Account(**data["account"])
            events: AccountEvents = AccountEvents(**data["events"])

            page = int(page.split(":")[1])
            current_page = data.get("page", 1)
            total_pages = int((len(events.events)) / 10)

            if page == current_page:
                await call.answer()
                return

            if page > total_pages:
                async with ThrottlingContext(bot=call.bot, state=state,
                                             chat_id=chat_id, message_id=message_id,
                                             emojis=EMOJIS_MAGNIFIER):
                    search: AccountEvents = await tonapi.accounts.get_events(
                        account_id=account.address.to_userfriendly(),
                        limit=10, before_lt=events.events[-1].lt,
                    )
                    events.events += search.events
                    total_pages += 1

            await state.update_data(
                page=page, total_pages=total_pages, events=events.dict()
            )
            await windows.events_page(
                bot=call.bot, state=state,
                chat_id=chat_id, message_id=message_id,
            )

    await call.answer()


@rate_limit(1)
async def information_event(call: CallbackQuery, state: FSMContext, chat_id, message_id) -> None:
    data = await state.get_data()

    match call.data:
        case callback_data.back:
            from_pages = data.get("from_pages", False)
            if from_pages:
                await windows.events_page(
                    bot=call.bot, state=state,
                    chat_id=chat_id, message_id=message_id,
                )
            else:
                await windows.main(
                    bot=call.bot, state=state,
                    chat_id=chat_id, message_id=message_id,
                )
        case callback_data.show_json:
            try:
                await windows.information_event_json(
                    bot=call.bot, state=state,
                    chat_id=chat_id, message_id=message_id,
                )
            except (MessageIsTooLong, BadRequestMessageIsTooLong):
                text = messages.call__json_too_long
                await call.answer(text, show_alert=True)

    await call.answer()


@rate_limit(1)
async def information_event_json(call: CallbackQuery, state: FSMContext, chat_id, message_id) -> None:
    match call.data:
        case callback_data.back:
            await windows.information_event(
                bot=call.bot, state=state,
                chat_id=chat_id, message_id=message_id,
            )

    await call.answer()


@rate_limit(0.5)
async def select_date(call: CallbackQuery, state: FSMContext, chat_id, message_id) -> None:
    data = await state.get_data()

    current_date = datetime.datetime.now()

    start_date = data.get("start_date", None)
    end_date = data.get("end_date", None)
    date = data.get("date", current_date.timestamp())

    date = datetime.datetime.fromtimestamp(date)
    start_date = datetime.datetime.fromtimestamp(start_date) if start_date else None
    end_date = datetime.datetime.fromtimestamp(end_date) if end_date else None

    match call.data:
        case InlineKeyboardCalendar.cb_back:
            await state.update_data(start_date=None, end_date=None)
            await windows.events_page(
                bot=call.bot, state=state,
                chat_id=chat_id, message_id=message_id,
            )

        case InlineKeyboardCalendar.cb_next:
            await windows.confirm_export(
                bot=call.bot, state=state,
                chat_id=chat_id, message_id=message_id,
            )
        case InlineKeyboardCalendar.cb_export_for_all_time:
            await state.update_data(start_date=None, end_date=None,
                                    all_time=call.data)
            await windows.confirm_export(
                bot=call.bot, state=state,
                chat_id=chat_id, message_id=message_id,
            )

        case cdata if cdata.startswith(InlineKeyboardCalendar.cb_year):
            if cdata == InlineKeyboardCalendar.cb_year:
                if start_date and end_date:
                    start_date, end_date = None, None
                else:
                    start_date = date.replace(month=1, day=1, hour=0, minute=0, second=0).timestamp()
                    last_day = calendar.monthrange(date.year, date.month)[1]
                    end_date = date.replace(month=12, day=last_day, hour=23, minute=59, second=59).timestamp()
                await state.update_data(
                    start_date=start_date, end_date=end_date
                )
                await windows.select_date(
                    bot=call.bot, state=state,
                    chat_id=chat_id, message_id=message_id,
                )
            else:
                match call.data.split(":")[1]:
                    case InlineKeyboardCalendar.cb_left:
                        date = date.replace(year=date.year - 1)
                    case InlineKeyboardCalendar.cb_right:
                        date = date.replace(year=date.year + 1)

                if date <= current_date:
                    await state.update_data(date=date.timestamp())
                    await windows.select_date(
                        bot=call.bot, state=state,
                        chat_id=chat_id, message_id=message_id,
                    )

        case cdata if cdata.startswith(InlineKeyboardCalendar.cb_month):
            if cdata == InlineKeyboardCalendar.cb_month:
                if start_date and end_date:
                    start_date, end_date = None, None
                else:
                    start_date = date.replace(day=1, hour=0, minute=0, second=0).timestamp()
                    last_day = calendar.monthrange(date.year, date.month)[1]
                    end_date = date.replace(day=last_day, hour=23, minute=59, second=59).timestamp()
                await state.update_data(
                    start_date=start_date, end_date=end_date
                )
                await windows.select_date(
                    bot=call.bot, state=state,
                    chat_id=chat_id, message_id=message_id,
                )
            else:
                match call.data.split(":")[1]:
                    case InlineKeyboardCalendar.cb_left:
                        month = date.month - 1 if date.month > 1 else date.month
                    case _:
                        month = date.month + 1 if date.month < 12 else date.month
                date = date.replace(month=month)

                if date <= current_date:
                    await state.update_data(date=date.timestamp())
                    await windows.select_date(
                        bot=call.bot, state=state,
                        chat_id=chat_id, message_id=message_id,
                    )

        case cdata if cdata.startswith(InlineKeyboardCalendar.cb_day):
            day = int(call.data.split(":")[1])
            if date <= current_date:
                if start_date and end_date:
                    start_date, end_date = None, None
                elif not start_date:
                    start_date, end_date = date.replace(day=day, hour=0, minute=0, second=0).timestamp(), None
                else:
                    start_date = start_date.timestamp()
                    end_date = date.replace(day=day, hour=23, minute=59, second=59).timestamp()
                    if start_date > end_date:
                        start_date, end_date = None, None
                await state.update_data(
                    start_date=start_date, end_date=end_date, date=date.timestamp(),
                )
                await windows.select_date(
                    bot=call.bot, state=state,
                    chat_id=chat_id, message_id=message_id,
                )

    await call.answer()


@rate_limit(1)
async def confirm_export(call: CallbackQuery, state: FSMContext, tonapi: AsyncTonapi, chat_id, message_id) -> None:
    data = await state.get_data()

    match call.data:
        case callback_data.back:
            await state.update_data(all_time=False)
            await windows.select_date(
                bot=call.bot, state=state,
                chat_id=chat_id, message_id=message_id,
            )
        case callback_data.go_main:
            await windows.main(
                bot=call.bot, state=state,
                chat_id=chat_id, message_id=message_id,
            )
        case callback_data.confirm:
            try:
                async with ThrottlingContext(bot=call.bot, state=state,
                                             chat_id=chat_id, message_id=message_id,
                                             emojis=EMOJIS_MAGNIFIER):
                    account: Account = Account(**data["account"])

                    start_date = data.get("start_date", None)
                    end_date = data.get("end_date", None)
                    all_time = data.get("all_time", None)

                    next_from, amount_received, amount_sent = None, 0, 0
                    start_export_date = datetime.datetime.now()
                    events = AccountEvents(events=[], next_from=0)

                    while True:
                        if not all_time:
                            search = await tonapi.accounts.get_events(
                                account_id=account.address.to_userfriendly(),
                                start_date=int(str(start_date).split(".")[0]),
                                end_date=int(str(end_date).split(".")[0]),
                                before_lt=next_from, limit=1000,
                            )
                        else:
                            search = await tonapi.accounts.get_events(
                                account_id=account.address.to_userfriendly(),
                                before_lt=next_from, limit=1000,
                            )
                        if len(search.events) == 0 or search.next_from == 0:
                            break

                        for event in search.events:
                            if event.actions[0].TonTransfer:
                                amount = float(event.actions[0].simple_preview.value.split(" ")[0])
                                if event.actions[0].TonTransfer.sender.address.to_userfriendly() == \
                                        account.address.to_userfriendly():
                                    amount_sent += amount
                                else:
                                    amount_received += amount

                        next_from = search.next_from
                        events.events += search.events
                        await asyncio.sleep(1)

                    export_manager = ExportManager(events)
                    if data["export_type"] == callback_data.export_as_json:
                        document = await export_manager.save_as_json()
                    else:
                        document = await export_manager.save_as_csv()

                    end_export_date = datetime.datetime.now()
                    time_spent_seconds = (end_export_date - start_export_date).total_seconds()
                    time_spent = str(datetime.timedelta(seconds=time_spent_seconds)).split(".")[0]
                    price = (await Coingecko().get()).ton.usd

                    if not all_time:
                        caption = messages.export_completed.format(
                            address=account.address.to_userfriendly(),
                            start_date=datetime.datetime.fromtimestamp(start_date).strftime("%Y-%m-%d %H:%M"),
                            end_date=datetime.datetime.fromtimestamp(end_date).strftime("%Y-%m-%d %H:%M"),
                            export_type=getattr(buttons, data["export_type"]).split(" ")[3],
                            total_rows=len(events.events),
                            time_spent=time_spent,
                            amount_sent=f"{amount_sent:,.2f} {(amount_sent * price):,.2f}",
                            amount_received=f"{amount_received:,.2f} {(amount_received * price):,.2f}",
                        )
                    else:
                        caption = messages.confirm_export_all_time_completed.format(
                            address=account.address.to_userfriendly(),
                            export_date=InlineKeyboardCalendar.export_for_all_time,
                            export_type=getattr(buttons, data["export_type"]),
                            total_rows=len(events.events),
                            time_spent=time_spent,
                            amount_sent=f"{amount_sent:,.2f} ≈ ${(amount_sent * price):,.2f}",
                            amount_received=f"{amount_received:,.2f} ≈ ${(amount_received * price):,.2f}",
                        )

                await call.message.answer_document(document=document, caption=caption)
                await delete_previous_message(bot=call.bot, state=state)
                await windows.main(
                    bot=call.bot, state=state,
                    chat_id=chat_id, message_id=message_id,
                )

            except (Exception,) as error:
                text = messages.export_failed.format(error=error)
                markup = inline.go_main()
                await edit_or_send_message(
                    bot=call.bot, state=state,
                    chat_id=chat_id, message_id=message_id,
                    text=text, markup=markup,
                )
                raise

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
        information_event, IsPrivate(),
        state=State.information_event,
    )
    dp.register_callback_query_handler(
        information_event_json, IsPrivate(),
        state=State.information_event_json,
    )
    dp.register_callback_query_handler(
        select_date, IsPrivate(),
        state=State.select_date,
    )
    dp.register_callback_query_handler(
        confirm_export, IsPrivate(),
        state=State.confirm_export,
    )
    dp.register_callback_query_handler(
        main, IsPrivate(),
        state="*",
    )

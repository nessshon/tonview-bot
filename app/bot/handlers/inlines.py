import logging

from aiogram import Dispatcher
from aiogram.types import InlineQuery
from aiogram.utils.parts import paginate
from pytonapi import AsyncTonapi
from pytonapi.exceptions import TONAPIUnauthorizedError, TONAPITooManyRequestsError, TONAPIBadRequestError

from app.bot.keyboards import inline
from app.bot.texts import articles, messages
from app.bot.texts.articles import create_contract_article


async def inline_query_handler(inline_query: InlineQuery, tonapi: AsyncTonapi):
    try:
        match inline_query.query:
            case query if query.startswith("events"):
                offset = inline_query.offset or 0
                account_id = query.split(" ")[1]

                items = await tonapi.accounts.get_events(
                    account_id=account_id, before_lt=offset, limit=50,
                )
                nft_addresses = {
                    event.event_id: event.actions[0].NftItemTransfer.nft
                    for event in items.events if event.actions[0].NftItemTransfer
                }
                if any(nft_addresses):
                    search = await tonapi.nft.get_bulk_items(list(nft_addresses.values()))
                    [
                        event.actions[0].NftItemTransfer.__setattr__('nft', nft) for event in items.events if
                        event.actions[0].NftItemTransfer and (nft_address := nft_addresses.get(event.event_id))
                        for nft in search.nft_items if nft.address.to_raw() == nft_address
                    ]

                results = [articles.create_event_article(item) for item in items.events]
                if results:
                    next_offset = str(items.events[-1].lt)
                    await inline_query.answer(
                        results=results, cache_time=100, is_personal=True, next_offset=next_offset
                    )
            case query if query.startswith("collectibles"):
                offset = int(inline_query.offset) if inline_query.offset else 0
                account_id = query.split(" ")[1]

                items = await tonapi.accounts.get_nfts(
                    account_id=account_id, limit=50,
                    offset=offset, indirect_ownership=True,
                )
                results = [articles.create_collectible(item) for item in
                           sorted(items.nft_items, key=lambda item: item.index)]
                if results:
                    next_offset = str(offset + 50)
                    await inline_query.answer(
                        results=results, cache_time=10, is_personal=True, next_offset=next_offset
                    )

            case query if query.startswith("tokens"):
                offset = int(inline_query.offset) if inline_query.offset else 0
                account_id = query.split(" ")[1]

                items = await tonapi.accounts.get_jettons_balances(account_id=account_id)
                items = paginate(items.balances, int(offset), 50)

                results = [articles.create_token(item) for item in items]
                results = [article for article in results if article]
                if results:
                    next_offset = str(offset + 50)
                    await inline_query.answer(
                        results=results, cache_time=10, is_personal=True, next_offset=next_offset
                    )

            case query if query.startswith("items"):
                offset = int(inline_query.offset) if inline_query.offset else 0
                account_id = query.split(" ")[1]

                items = await tonapi.nft.get_items_by_collection_address(
                    account_id=account_id, limit=50, offset=offset,
                )

                results = [articles.create_collectible(item) for item in
                           sorted(items.nft_items, key=lambda item: item.index)]
                if results:
                    next_offset = str(offset + 50)
                    await inline_query.answer(
                        results=results, cache_time=10, is_personal=True, next_offset=next_offset
                    )

            case query if query.startswith("holders"):
                offset = int(inline_query.offset) if inline_query.offset else 0
                account_id = query.split(" ")[1]

                jetton = await tonapi.jettons.get_info(account_id=account_id)
                items = await tonapi.jettons.get_holders(account_id=account_id)
                items = paginate(items.addresses, offset, 50)

                results = [articles.create_holders(jetton, item) for item in items]
                if results:
                    next_offset = str(offset + 50)
                    await inline_query.answer(
                        results=results, cache_time=10, is_personal=True, next_offset=next_offset
                    )
            case _:
                results = await contract_inline_query(inline_query, tonapi)
                await inline_query.answer(
                    results=[results], cache_time=10, is_personal=True
                )

    except Exception as e:
        logging.error(e)

    await inline_query.answer([], cache_time=10, is_personal=True)


async def contract_inline_query(inline_query: InlineQuery, tonapi: AsyncTonapi):
    try:
        match inline_query.query:
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
                    chl = f"ton://transfer/{account.address.to_userfriendly()}"
                    preview_url = f"https://chart.googleapis.com/chart?chs=512x512&cht=qr&chl={chl}"
                    message_text = messages.information(account, preview_url)
                    reply_markup = inline.information(account.address.to_userfriendly(), True)

                    return create_contract_article(account, message_text, reply_markup)

                case interfaces if "tep74" in interfaces:
                    jetton = await tonapi.jettons.get_info(account_id)
                    message_text = messages.information_jetton(account, jetton)
                    reply_markup = inline.information_jetton(account.address.to_userfriendly(), True)

                    return create_contract_article(account, message_text, reply_markup)

                case interfaces if "tep62_item" in interfaces:
                    nft = await tonapi.nft.get_item_by_address(account_id)
                    message_text = messages.information_nft(account, nft)
                    reply_markup = inline.information_nft(account.address.to_userfriendly(), True)

                    return create_contract_article(account, message_text, reply_markup)

                case interfaces if "tep62_collection" in interfaces:
                    collection = await tonapi.nft.get_collection_by_collection_address(account_id)
                    message_text = messages.information_collection(account, collection)
                    reply_markup = inline.information_collection(account.address.to_userfriendly(), True)

                    return create_contract_article(account, message_text, reply_markup)

                case _:
                    chl = f"ton://transfer/{account.address.to_userfriendly()}"
                    preview_url = f"https://chart.googleapis.com/chart?chs=512x512&cht=qr&chl={chl}"
                    message_text = messages.information(account, preview_url)
                    reply_markup = inline.information(account.address.to_userfriendly(), True)

                    return create_contract_article(account, message_text, reply_markup)

    except (TONAPIUnauthorizedError, TONAPITooManyRequestsError):
        raise

    except Exception as e:
        if "encoding/hex" in str(e):
            pass
        else:
            raise

    return []


def register(dp: Dispatcher) -> None:
    dp.register_inline_handler(
        inline_query_handler, state="*"
    )

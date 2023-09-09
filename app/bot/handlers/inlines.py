import logging

from aiogram import Dispatcher
from aiogram.types import InlineQuery
from aiogram.utils.parts import paginate
from pytonapi import AsyncTonapi

from app.bot.texts import articles


async def inline_handler(inline: InlineQuery, tonapi: AsyncTonapi):
    try:
        match inline.query:
            case query if query.startswith("events"):
                offset = inline.offset or 0
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
                    await inline.answer(
                        results=results, cache_time=100, is_personal=True, next_offset=next_offset
                    )
            case query if query.startswith("collectibles"):
                offset = inline.offset or 0
                account_id = query.split(" ")[1]

                items = await tonapi.accounts.get_nfts(
                    account_id=account_id, limit=50,
                    offset=int(offset), indirect_ownership=True,
                )

                results = [articles.create_collectible(item) for item in items.nft_items]
                if results:
                    next_offset = str(int(offset) + 50)
                    await inline.answer(
                        results=results, cache_time=10, is_personal=True, next_offset=next_offset
                    )

            case query if query.startswith("tokens"):
                offset = inline.offset or 0
                account_id = query.split(" ")[1]

                items = await tonapi.accounts.get_jettons_balances(account_id=account_id)
                items = paginate(items.balances, int(offset), 50)

                results = [articles.create_token(item) for item in items]
                results = [article for article in results if article]
                if results:
                    next_offset = str(int(offset) + 1)
                    await inline.answer(
                        results=results, cache_time=10, is_personal=True, next_offset=next_offset
                    )

            case query if query.startswith("items"):
                offset = inline.offset or 0
                account_id = query.split(" ")[1]

                items = await tonapi.nft.get_items_by_collection_address(
                    account_id=account_id, limit=50, offset=int(offset),
                )

                results = [articles.create_collectible(item) for item in items.nft_items]
                if results:
                    next_offset = str(int(offset) + 1)
                    await inline.answer(
                        results=results, cache_time=10, is_personal=True, next_offset=next_offset
                    )

            case query if query.startswith("holders"):
                offset = inline.offset or 0
                account_id = query.split(" ")[1]

                jetton = await tonapi.jettons.get_info(account_id=account_id)
                items = await tonapi.jettons.get_holders(account_id=account_id)
                items = paginate(items.addresses, int(offset), 50)

                results = [articles.create_holders(jetton, item) for item in items]
                if results:
                    next_offset = str(int(offset) + 1)
                    await inline.answer(
                        results=results, cache_time=10, is_personal=True, next_offset=next_offset
                    )
    except Exception as e:
        logging.error(e)

    await inline.answer([], cache_time=10, is_personal=True)


def register(dp: Dispatcher) -> None:
    dp.register_inline_handler(
        inline_handler, state="*"
    )

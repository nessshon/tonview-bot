import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineQuery
from aiogram.utils.parts import paginate
from pytonapi import AsyncTonapi

from app.bot.texts import articles


async def inline_handler(inline: InlineQuery, tonapi: AsyncTonapi):
    try:
        match inline.query:
            case query if query.startswith("transactions"):
                offset = inline.offset or 0
                account_id = query.split(" ")[1]

                items = await tonapi.blockchain.get_account_transactions(
                    account_id=account_id, before_lt=offset, limit=50,
                )

                results = [articles.create_transaction(item) for item in items.transactions]
                if results:
                    next_offset = str(items.transactions[-1].lt)
                    await inline.answer(
                        results=results, cache_time=1, is_personal=True, next_offset=next_offset
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
                        results=results, cache_time=1, is_personal=True, next_offset=next_offset
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
                        results=results, cache_time=1, is_personal=True, next_offset=next_offset
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
                        results=results, cache_time=1, is_personal=True, next_offset=next_offset
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
                        results=results, cache_time=1, is_personal=True, next_offset=next_offset
                    )
    except Exception as e:
        logging.error(e)

    await inline.answer([], cache_time=1, is_personal=True)


def register(dp: Dispatcher) -> None:
    dp.register_inline_handler(
        inline_handler, state="*"
    )

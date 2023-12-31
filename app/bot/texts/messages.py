from datetime import datetime

from aiogram.utils.markdown import hide_link, hbold, hcode, hitalic, hlink
from pytonapi.schema.accounts import Account
from pytonapi.schema.events import Event
from pytonapi.schema.jettons import JettonInfo
from pytonapi.schema.nft import NftItem, NftCollection

from app.bot.utils.address import AddressDisplay
from app.bot.utils.links import GetgemsLink
from app.bot.utils.coingecko import Coingecko

main = (
    f"{hide_link('https://telegra.ph//file/1e7bbb0756d2bf7ba926a.jpg')}"
    f"{hlink(title='Tonviewer', url='https://tonviewer.com/')} <b>— the only explorer you need for TON</b>\n\n"
    "Send address, name or transaction:"
)

help = (
    f"{hide_link('https://telegra.ph//file/e13b6f90497a231bf3712.jpg')}"
    "<b>About the bot:</b>\n\n"
    "• TONViewBot is a Telegram bot inspired by tonviewer.com. "
    "It provides users with the ability to explore and retrieve information about blocks, "
    "transactions, and addresses on the TON blockchain.\n\n"

    f"• This bot utilizes the REST API from {hlink('tonapi.io', url='https://tonapi.io/api-v2')} "
    f"to fetch data from the blockchain. "
    "It also uses coingecko.com to fetch the current price of TON.\n\n"

    "<b>Main technology stack:</b>\n"
    f"• {hlink('python 3.10', 'https://www.python.org/downloads/release/python-3100/')}\n"
    f"• {hlink('pytonapi 0.1.1', 'https://pypi.org/project/pytonapi/')}\n"
    f"• {hlink('aiogram 2.25.1', 'https://pypi.org/project/aiogram/2.25.1/')}\n\n"
    "For any feedback or inquiries, please reach out to @NessFeedbackBot.\n"
)
call__switched_to_testnet = (
    "Switched to Testnet!"
)

switched_to_testnet = (
    f"{hide_link('https://telegra.ph//file/6cb848aa51c5fa3c8ca64.jpg')}"
    "<b>Switched to Testnet!</b>\n\n"
    "Search by address, name or transaction:"
)

call__switched_to_mainnet = (
    "Switched to Mainnet!"
)

switched_to_mainnet = (
    f"{hide_link('https://telegra.ph//file/9f577834cc7cd270ede04.jpg')}"
    "<b>Switched to Mainnet!\n\n</b>"
    "Send address, name or transaction:"
)

set_api_key = (
    f"{hide_link('https://telegra.ph//file/f8e0b2c6ea45c20a31c1a.jpg')}"
    "<b>Send your API key:</b>\n\n"
    "The bot has a shared API key that is used for all user requests. "
    "You can provide your own API key to speed up the processing of your requests.\n\n"
    "• Get an API key from tonconsole.com.\n\n"
    "<i>Your keys remain strictly confidential and are not shared with third parties. "
    "They are used solely between you and the bot. </i>"
)

call__api_key_removed = (
    "API key removed!"
)

api_key_invalid__input = (
    f"{hide_link('https://telegra.ph//file/0842a6e201b9b2d182979.jpg')}"
    "<b>Invalid API key, send correct API key:</b>\n\n"
    "• Get an API key from tonconsole.com."
)

api_key_invalid__error = (
    f"{hide_link('https://telegra.ph//file/0842a6e201b9b2d182979.jpg')}"
    "<b>Invalid API key!</b>\n\n"
    "Send new API key or remove existing:\n\n"
    "• Get an API key from tonconsole.com."
)
too_many_requests__error = (
    f"{hide_link('https://telegra.ph//file/da188a306888acb19f1ae.jpg')}"
    "<b>Rate limit exceeded!</b>\n\n"
    "• Please try again later, or set your API key."
)

not_found = (
    f"{hide_link('https://telegra.ph//file/2e6bd84cd0ef81f879e5d.jpg')}"
    "<b>Sorry, didn't find any result!</b>\n\n"
    "Make sure your query is correct, that the correct network is selected, and search again."
)

call__attributes_not_found = "Attributes not found!"

call__json_too_long = "JSON is too long to fit in a message!"
call__metadata_too_long = "Metadata is too long to fit in a message!"
call__attributes_too_long = "Attributes is too long to fit in a message!"
call__need_api_key = "To export you need to set your API key!"

contract_events = (
    f"{hide_link('https://telegra.ph//file/466f2347ff0b174973902.jpg')}"
    "<b>Transactions history:</b>\n\n"
    f"• {hbold('Account:')}\n"
    "<code>{address}</code>"
)

no_more_pages = "This is the last page."

events_page = (
    f"{hide_link('https://telegra.ph//file/26d99fcbfd04a3657606b.jpg')}"
    f"• {hbold('Account:')}\n"
    f"{hcode('{address}')}\n\n"
    f"{hbold('Transactions history:')}\n"
)

select_date = (
    f"{hide_link('https://telegra.ph//file/27cfb15b59be2527f26b1.jpg')}"
    "<b>Select date range to export:</b>\n\n"
    f"• {hbold('Start date:')}\n"
    f"{hcode('{start_date}')}\n\n"
    f"• {hbold('End date:')}\n"
    f"{hcode('{end_date}')}"
)

confirm_export = (
    f"{hide_link('https://telegra.ph//file/15ad871627114c4baee13.jpg')}"
    "<b>Export details:</b>\n\n"
    f"• {hbold('Start date:')}\n"
    f"{hcode('{start_date}')}\n\n"
    f"• {hbold('End date:')}\n"
    f"{hcode('{end_date}')}\n\n"
    f"• {hbold('Export type:')}\n"
    f"{hcode('{export_type}')}\n\n"
    f"{hbold('Confirm export?')}\n"
)
confirm_export_all_time = (
    f"{hide_link('https://telegra.ph//file/15ad871627114c4baee13.jpg')}"
    "<b>Export details:</b>\n\n"
    f"{hbold('{export_date}')}\n\n"
    f"• {hbold('Export type:')}\n"
    f"{hcode('{export_type}')}\n\n"
    f"{hbold('Confirm export?')}\n"
)
export_completed = (
    "#Export\n\n"
    f"• {hbold('Address:')}\n"
    f"{hcode('{address}')}\n\n"
    f"• {hbold('Start date:')}\n"
    f"{hcode('{start_date}')}\n\n"
    f"• {hbold('End date:')}\n"
    f"{hcode('{end_date}')}\n\n"
    f"• {hbold('Export type:')}\n"
    f"{hcode('{export_type}')}\n\n"
    f"• {hbold('Total rows:')}\n"
    f"{hcode('{total_rows}')}\n\n"
    f"• {hbold('Time spent:')}\n"
    f"{hcode('{time_spent}')}\n\n"
    f"• {hbold('Total sent:')}\n"
    f"{hcode('{amount_sent} TON')}\n\n"
    f"• {hbold('Total received:')}\n"
    f"{hcode('{amount_received} TON')}"
)

confirm_export_all_time_completed = (
    "#Export\n\n"
    f"• {hbold('Address:')}\n"
    f"{hcode('{address}')}\n\n"
    f"• {hbold('Export date:')}\n"
    f"{hcode('{export_date}')}\n\n"
    f"• {hbold('Export type:')}\n"
    f"{hcode('{export_type}')}\n\n"
    f"• {hbold('Total rows:')}\n"
    f"{hcode('{total_rows}')}\n\n"
    f"• {hbold('Time spent:')}\n"
    f"{hcode('{time_spent}')}\n\n"
    f"• {hbold('Total sent:')}\n"
    f"{hcode('{amount_sent}')}\n\n"
    f"• {hbold('Total received:')}\n"
    f"{hcode('{amount_received}')}"
)

export_failed = (
    f"{hide_link('https://telegra.ph//file/19bf4c4724bb1aa803fa1.jpg')}"
    f"{hbold('Export failed!')}\n\n"
    f"• {hbold('Error:')}\n"
    f"{hcode('{error}')}"
)


async def information(account: Account, preview: str) -> str:
    price = (await Coingecko().get()).ton.usd

    amount = account.balance.to_amount(8)

    return (
        f"{hide_link(preview)}"
        f"{hide_link('https://telegra.ph//file/784afcdf40bff1e0f06f9.jpg')}"
        f"• {hbold('Status:')}\n"
        f"{hcode(account.status)}\n\n"
        f"• {hlink('Balance', url='https://www.coingecko.com/en/coins/toncoin')}:\n"
        f"{hcode(f'{amount:,.6f}')} TON {hcode(f'≈ ${round(amount * price, 2):,.2f}')}\n\n"
        f"• {hlink('Account', url='https://tonviewer.com/' + account.address.to_userfriendly())}:\n"
        f"{hcode(AddressDisplay(account).title())}\n\n"
        f"• {hbold('Raw:')}\n"
        f"{hcode(account.address.to_raw())}\n\n"
        f"• {hbold('Contract type:')}\n"
        f"{hcode(', '.join(i for i in account.interfaces) if account.interfaces else 'Unknown')}\n\n"
    )


async def information_jetton(account: Account, jetton: JettonInfo) -> str:
    preview = jetton.metadata.image if jetton.metadata.image else "https://telegra.ph//file/784afcdf40bff1e0f06f9.jpg"
    preview = f"https://ipfs.io/ipfs/{preview}" if preview.startswith("ipfs://") else preview
    text = await information(account, preview)
    total_supply = round(int(jetton.total_supply) / 10 ** int(jetton.metadata.decimals), 4)

    description = (
        jetton.metadata.description if jetton.metadata.description else None
    )
    text += (
        f"• {hbold('Jetton name:')}\n"
        f"{hcode(jetton.metadata.name)}\n\n"
    )
    if description: text += (  # noqa:E701
        f"• {hbold('Description:')}\n"
        f"{hitalic(description)}\n\n"
    )
    text += (
        f"• {hbold('Mintable:')}\n"
        f"{hcode(jetton.mintable)}\n\n"
        f"• {hbold('Max. supply:')}\n"
        f"{hcode(f'{float(total_supply):,.2f}')} {jetton.metadata.symbol}\n\n"
    )

    return text


async def information_nft(account: Account, nft: NftItem) -> str:
    preview = nft.previews[-1].url if len(nft.previews) > 1 else "https://telegra.ph//file/784afcdf40bff1e0f06f9.jpg"
    text = await information(account, preview)

    name = nft.dns if nft.dns else nft.metadata["name"] if "name" in nft.metadata else "Unknown"
    if name != "Unknown": name = GetgemsLink.nft(name, nft.address.to_userfriendly())  # noqa:E701
    text += (
        f"• {hbold('NFT Name:')}\n"
        f"{name}\n\n"
    )
    description = nft.metadata["description"] if "description" in nft.metadata else None
    if description: text += (  # noqa:E701
        f"• {hbold('Description:')}\n"
        f"{hitalic(description)}\n\n"
    )
    collection = nft.collection.name if nft.collection and nft.collection else None
    if collection: text += (  # noqa:E701
        f"• {hbold('Collection:')}\n"
        f"{GetgemsLink.collection(collection, nft.collection.address.to_userfriendly())}\n\n"
    )
    if collection: text += (  # noqa:E701
        f"• {hbold('Collection address:')}\n"
        f"{hcode(nft.collection.address.to_userfriendly())}\n\n"
    )
    if nft.owner: text += (  # noqa:E701
        f"• {hbold('Owner address:')}\n"
        f"{hcode(nft.owner.address.to_userfriendly())}\n\n"
    )

    return text


async def information_collection(account: Account, collection: NftCollection) -> str:
    preview = (
        collection.previews[-1].url if any(collection.previews)
        else "https://telegra.ph//file/784afcdf40bff1e0f06f9.jpg"
    )
    text = await information(account, preview)

    name = collection.metadata["name"] if "name" in collection.metadata else "Unknown"
    if name != "Unknown": name = GetgemsLink.collection(name, collection.address.to_userfriendly())  # noqa:E701
    text += (
        f"• {hbold('Collection Name:')}\n"
        f"{name}\n\n"
    )
    description = collection.metadata["description"] if "description" in collection.metadata else None
    if description: text += (  # noqa:E701
        f"• {hbold('Description:')}\n"
        f"{hitalic(description)}\n\n"
    )
    if collection.next_item_index:
        text += (
            f"• {hbold('Items:')}\n"
            f"{hcode(collection.next_item_index)}\n\n"
        )
    if collection.owner: text += (  # noqa:E701
        f"• {hbold('Owner address:')}\n"
        f"{hcode(collection.owner.address.to_userfriendly())}\n\n"
    )

    return text


async def contract_event(event: Event):
    text = (
        f"• {hbold('Timestamp:')}\n"
        f"{hcode(datetime.fromtimestamp(event.timestamp).strftime('%d.%m.%Y, %H:%M:%S'))}\n\n"
    )

    for action in event.actions:
        text += (
            f"• {hbold('Action:')}\n"
            f"{action.simple_preview.name}\n"
            f"• {hbold('Route:')}\n"
        )

        if len(action.simple_preview.accounts) == 2:
            text += (
                f"{AddressDisplay(action.simple_preview.accounts[0]).short_link()} → "
                f"{AddressDisplay(action.simple_preview.accounts[1]).short_link()}\n"
            )
        else:
            text += (
                f"{AddressDisplay(action.simple_preview.accounts[0]).short_link()}\n"
            )

        if action.simple_preview.value:
            text += (
                f"• {hbold('Value:')}\n"
                f"{hcode(action.simple_preview.value)}\n\n"
            )
        else:
            text += "\n"

    text += (
        f"• {hbold('hash:')}\n"
        f"{hcode(event.event_id)}\n"
    )
    return text

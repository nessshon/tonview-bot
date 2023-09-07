from datetime import datetime

from aiogram.utils.markdown import hide_link, hbold, hcode, hitalic, hlink
from pytonapi.schema.accounts import Account
from pytonapi.schema.jettons import JettonInfo
from pytonapi.schema.nft import NftItem, NftCollection
from pytonapi.schema.traces import Transaction
from pytonapi.utils import nano_to_amount

from app.bot.utils.links import GetgemsLink

main = (
    f"{hide_link('https://telegra.ph//file/1e7bbb0756d2bf7ba926a.jpg')}"
    f"{hlink(title='Tonviewer', url='https://tonviewer.com/')} <b>— the only explorer you need for TON</b>\n\n"
    "Search by address, name or transaction:"
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
    "Search by address, name or transaction:"
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
    f"{hide_link('https://telegra.ph//file/39269417eea2853eb4f34.jpg')}"
    "<b>Invalid API key, send correct API key:</b>\n\n"
    "• Get an API key from tonconsole.com."
)

api_key_invalid__error = (
    f"{hide_link('https://telegra.ph//file/39269417eea2853eb4f34.jpg')}"
    "<b>Invalid API key!</b>\n\n"
    "Send new API key or remove existing:\n\n"
    "• Get an API key from tonconsole.com."
)

not_found = (
    f"{hide_link('https://telegra.ph//file/fa24c09522153e3b2273e.jpg')}"
    "<b>Sorry, didn't find any result!</b>\n\n"
    "Make sure your query is correct, that the correct network is selected, and search again."
)

call__attributes_not_found = "Attributes not found!"
call__json_too_long = "JSON is too long to fit in a message!"

contract_transactions = (
    f"{hide_link('https://telegra.ph//file/466f2347ff0b174973902.jpg')}"
    "<b>Transactions history:</b>\n\n"
    f"• {hbold('Address:')}\n"
    "<code>{address}</code>"
)

no_more_transactions = "This is the last page, no more transactions."


def information(account: Account, preview: str) -> str:
    return (
        f"{hide_link(preview)}"
        f"{hide_link('https://telegra.ph//file/784afcdf40bff1e0f06f9.jpg')}"
        f"• {hbold('Status:')}\n"
        f"{hcode(account.status)}\n\n"
        f"• {hbold('Balance:')}\n"
        f"{hcode(account.balance.to_amount(8))} TON\n\n"
        f"• {hbold('Contract type:')}\n"
        f"{hcode(', '.join(i for i in account.interfaces))}\n\n"
        f"• {hbold('Address:')}\n"
        f"{hcode(account.address.to_userfriendly())}\n\n"
        f"• {hbold('Raw:')}\n"
        f"{hcode(account.address.to_raw())}\n\n"
    )


def information_jetton(account: Account, jetton: JettonInfo) -> str:
    preview = jetton.metadata.image if jetton.metadata.image else "https://telegra.ph//file/784afcdf40bff1e0f06f9.jpg"
    preview = f"https://ipfs.io/ipfs/{preview}" if preview.startswith("ipfs://") else preview
    text = information(account, preview)
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


def information_nft(account: Account, nft: NftItem) -> str:
    preview = nft.previews[-1].url if len(nft.previews) > 1 else "https://telegra.ph//file/784afcdf40bff1e0f06f9.jpg"
    text = information(account, preview)

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


def information_collection(account: Account, collection: NftCollection) -> str:
    preview = collection.metadata["image"] if "image" else "https://telegra.ph//file/784afcdf40bff1e0f06f9.jpg"
    text = information(account, preview)

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


def contract_transaction(transaction: Transaction):
    text = (
        f"• {hbold('Timestamp:')}\n"
        f"{hcode(datetime.fromtimestamp(transaction.utime).strftime('%d.%m.%Y, %H:%M:%S'))}\n\n"
    )

    if any(transaction.out_msgs):
        action = f"Sent TON"
        destination = (
            transaction.out_msgs[0].destination.address.to_userfriendly()
            if transaction.out_msgs[0].destination else None
        )
        source = (
            transaction.out_msgs[0].source.address.to_userfriendly()
            if transaction.out_msgs[0].source else None
        )
        comment = (
            transaction.out_msgs[0].decoded_body.get("text")
            if transaction.out_msgs[0].decoded_op_name == "text_comment" else None
        )
        amount = nano_to_amount(transaction.out_msgs[0].value, 8)
    else:
        action = "Received TON"
        destination = (
            transaction.in_msg.destination.address.to_userfriendly()
            if transaction.in_msg.destination else None
        )
        source = (
            transaction.in_msg.source.address.to_userfriendly()
            if transaction.in_msg.source else None
        )
        comment = (
            transaction.in_msg.decoded_body.get("text")
            if transaction.in_msg.decoded_op_name == "text_comment" else None
        )
        amount = nano_to_amount(transaction.in_msg.value, 8)

    text += (
        f"• {hbold('Action:')}\n"
        f"{action}\n\n"
    )
    if source: text += (  # noqa:E701
        f"• {hbold('Source:')}\n"
        f"{hcode(source)} \n\n"
    )
    if destination: text += (  # noqa:E701
        f"• {hbold('Destination:')}\n"
        f"{hcode(destination)} \n\n"
    )
    if comment: text += (  # noqa:E701
        f"• {hbold('Comment:')}\n"
        f"{hcode(comment)}\n\n"
    )
    text += (
        f"• {hbold('Amount:')}\n"
        f"{amount} TON\n\n"
    )
    text += (
        f"• {hbold('Hash:')}\n"
        f"{hcode(transaction.hash)}"
    )
    return text

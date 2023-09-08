from datetime import datetime

from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from pytonapi.schema.events import AccountEvent
from pytonapi.schema.jettons import JettonBalance, JettonHolder, JettonInfo
from pytonapi.schema.nft import NftItem

from app.bot.utils.address import AddressDisplay


def create_transaction(event: AccountEvent) -> InlineQueryResultArticle:
    timestamp = f"{datetime.fromtimestamp(event.timestamp).strftime('%d %b, %H:%M')} "
    action = event.actions[0]

    title = action.simple_preview.description
    description = f"{timestamp}\n"
    thumb_url = action.simple_preview.value_image

    if action.TonTransfer:
        sender = action.TonTransfer.sender
        recipient = action.TonTransfer.recipient
        if event.account.address.to_userfriendly() == sender.address.to_userfriendly():
            title = f"↑ Sent - {action.simple_preview.value}"
        else:
            title = f"↓ Received + {action.simple_preview.value}"
        description += f"• {AddressDisplay(sender).short()} → {AddressDisplay(recipient).short()}\n"
        description += f"• {action.TonTransfer.comment}" if action.TonTransfer.comment else ""

    elif action.JettonTransfer:
        sender = action.JettonTransfer.sender
        recipient = action.JettonTransfer.recipient
        if event.account.address.to_userfriendly() == sender.address.to_userfriendly():
            title = f"↑ Sent - {action.simple_preview.value}"
        else:
            title = f"↓ Received + {action.simple_preview.value}"
        description += f"• {AddressDisplay(sender).short()} → {AddressDisplay(recipient).short()}\n"
        description += f"• {action.JettonTransfer.comment}" if action.JettonTransfer.comment else ""

    elif action.ContractDeploy:
        title = action.simple_preview.name
        description += "• Interfaces: " + ", ".join(action.ContractDeploy.interfaces)

    elif action.JettonMint:
        ...

    elif action.JettonBurn:
        ...

    elif action.NftItemTransfer:
        sender = action.NftItemTransfer.sender
        recipient = action.NftItemTransfer.recipient
        nft: NftItem = action.NftItemTransfer.nft  # noqa
        nft_name = nft.dns or nft.metadata["name"] if nft.metadata else "Unknown"
        if event.account.address.to_userfriendly() == sender.address.to_userfriendly():
            title = f"↑ Sent NFT {nft_name}"
        else:
            title = f"↓ Received NFT {nft_name}"
        description += f"• {AddressDisplay(sender).short()} → {AddressDisplay(recipient).short()}"
        thumb_url = nft.previews[-1].url

    elif action.NftPurchase:
        nft: NftItem = action.NftPurchase.nft
        seller = action.NftPurchase.seller
        buyer = action.NftPurchase.buyer
        nft_name = nft.dns or nft.metadata["name"] if nft.metadata else "Unknown"
        title = f"↓ Purchased NFT {nft_name}"
        description += f"• {AddressDisplay(seller).short()} → {AddressDisplay(buyer).short()}\n"
        if action.NftPurchase.amount:
            description += f"• Price: {action.simple_preview.value}"
        thumb_url = nft.previews[-1].url

    return InlineQueryResultArticle(
        title=title,
        id=event.event_id,
        description=description,
        thumb_url=thumb_url,
        input_message_content=InputTextMessageContent(
            message_text=event.event_id,
        )
    )


def create_holders(jetton: JettonInfo, holder: JettonHolder) -> InlineQueryResultArticle:
    holder_address = holder.address.to_userfriendly()
    holder_balance = round(int(holder.balance) / 10 ** int(jetton.metadata.decimals), 2)

    title = (
        f"{holder_address[0:8]}. . .{holder_address[-6:]} - {holder_balance:,} {jetton.metadata.symbol}"
    )
    description = (
        f"{jetton.metadata.name or 'Unknown'} "
        "• Verified" if jetton.verification == "whitelist" else "• Not Verified"
    )
    thumb_url = jetton.metadata.image if jetton.metadata.image else "https://telegra.ph//file/784afcdf40bff1e0f06f9.jpg"
    thumb_url = f"https://ipfs.io/ipfs/{thumb_url}" if thumb_url.startswith("ipfs://") else thumb_url

    return InlineQueryResultArticle(
        title=title,
        id=holder_address,
        description=description,
        thumb_url=thumb_url,
        input_message_content=InputTextMessageContent(
            message_text=jetton.metadata.address.to_userfriendly(),
        )
    )


def create_collectible(nft: NftItem) -> InlineQueryResultArticle:
    title = (
        nft.dns if nft.dns else nft.metadata.get("name", "Unknown")
    )
    collection = (
        nft.collection.name if nft.collection else None
    )
    description = nft.metadata.get("description", "")
    description = f"• Collection: {collection}\n\n{description}" if collection else description

    return InlineQueryResultArticle(
        title=title,
        id=nft.address.to_userfriendly(),
        description=description,
        thumb_url=nft.previews[-1].url,
        input_message_content=InputTextMessageContent(
            message_text=nft.address.to_userfriendly(),
        )
    )


def create_token(jetton: JettonBalance) -> None | InlineQueryResultArticle:
    jetton_address = jetton.jetton.address.to_userfriendly()
    jetton_balance = round(int(jetton.balance) / 10 ** jetton.jetton.decimals, 2)
    if jetton_balance == 0:
        return

    jetton_name = (
        jetton.jetton.name if jetton.jetton and jetton.jetton.name else "Unknown"
    )
    jetton_symbol = (
        jetton.jetton.symbol if jetton.jetton and jetton.jetton.symbol else "UNKNOWN"
    )

    title = f"{jetton_name} - {jetton_balance:,} {jetton_symbol}"
    description = "• Verified" if jetton.jetton.verification == "whitelist" else "• Not Verified"
    thumb_url = (
        f"https://ipfs.io/ipfs/{jetton.jetton.image[7:]}" if jetton.jetton.image.startswith("ipfs://")
        else jetton.jetton.image
    )

    return InlineQueryResultArticle(
        title=title,
        id=jetton_address,
        description=description,
        thumb_url=thumb_url,
        input_message_content=InputTextMessageContent(
            message_text=jetton_address,
        )
    )

from datetime import datetime

from aiogram.types import InlineQueryResultArticle, InputTextMessageContent
from pytonapi.schema.blockchain import Transaction
from pytonapi.schema.jettons import JettonBalance, JettonHolder, JettonInfo
from pytonapi.schema.nft import NftItem
from pytonapi.utils import nano_to_amount


def create_transaction(transaction: Transaction) -> InlineQueryResultArticle:
    timestamp = f"{datetime.fromtimestamp(transaction.utime).strftime('%d %b, %H:%M')} "

    if any(transaction.out_msgs):
        action = "↑ {} Sent - {} TON"
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
        amount = nano_to_amount(transaction.out_msgs[0].value, 4)
    else:
        action = "↓ {} Received + {} TON"
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
        amount = nano_to_amount(transaction.in_msg.value, 4)

    title = action.format(timestamp, amount)
    description = (
        f"{source[0:6]}. . .{source[-4:]} → {destination[0:6]}. . .{destination[-4:]}"
    )
    description += (
        f"\n\n• {f'{comment[:35]}...' if len(comment) > 35 else comment}"
        if comment else ""
    )
    return InlineQueryResultArticle(
        title=title,
        id=transaction.hash,
        description=description,
        input_message_content=InputTextMessageContent(
            message_text=transaction.hash,
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

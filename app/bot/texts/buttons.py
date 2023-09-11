from datetime import datetime

from pytonapi.schema.events import AccountEvent

from ..utils.address import AddressDisplay

back = "‹ Back"

confirm = "✓ Confirm"

go_main = "‹ Go to main"

terms = "• Terms of use"

privacy = "• Privacy policy"

set_api_key = "• Set API key"

del_api_key = "• Remove API key"

switch_to_mainnet = "Switch to Mainnet"

switch_to_testnet = "Switch to Testnet"

tokens = "• Tokens"

collectibles = "• Collectibles"

events = "• Transaction history"

open_in_inline_mode = "• View in expanded list"

show_json = "• Show JSON"

metadata = "• Metadata"

attributes = "• Attributes"

items = "• Items"

holders = "• Holders"

export_as_json = "• Export as JSON"

export_as_csv = "• Export as CSV"


def create_event_button(event: AccountEvent) -> str:
    timestamp = datetime.fromtimestamp(event.timestamp).strftime('%d %b, %H:%M')
    action = event.actions[0]

    button = f"[ {timestamp} ]  •  {action.simple_preview.description}"

    if action.TonTransfer or action.JettonTransfer:
        sender = action.TonTransfer.sender if action.TonTransfer else action.JettonTransfer.sender
        recipient = action.TonTransfer.recipient if action.TonTransfer else action.JettonTransfer.recipient

        if event.account.address.to_userfriendly() == sender.address.to_userfriendly():
            button = (
                f"[ {timestamp} ]"
                f"    to {AddressDisplay(recipient).short(3, 4)}"
                f"    - {action.simple_preview.value}"
            )
        else:
            button = (
                f"[ {timestamp} ]"
                f"    from {AddressDisplay(sender).short(3, 4)}"
                f"    + {action.simple_preview.value}"
            )

    elif action.ContractDeploy:
        button = (
            f"[ {timestamp} ]"
            f"• {action.simple_preview.name} "
            f"{', '.join(action.ContractDeploy.interfaces)}"
        )

    elif action.JettonMint:
        ...

    elif action.JettonBurn:
        ...

    elif action.NftItemTransfer:
        sender = action.NftItemTransfer.sender
        recipient = action.NftItemTransfer.recipient

        if event.account.address.to_userfriendly() == sender.address.to_userfriendly():
            button = (
                f"[ {timestamp} ]"
                f"    to {AddressDisplay(recipient).short(3, 4)}"
                f"    - {action.simple_preview.value}"
            )
        else:
            button = (
                f"[ {timestamp} ]"
                f"    from {AddressDisplay(sender).short(3, 4)}"
                f"    + {action.simple_preview.value}"
            )

    elif action.NftPurchase:
        seller = action.NftPurchase.seller
        buyer = action.NftPurchase.buyer
        if event.account.address.to_userfriendly() == seller.address.to_userfriendly():
            button = (
                f"[ {timestamp} ]"
                f"Sold"
                f"    to {AddressDisplay(buyer).short(3, 4)}"
                f"    - {action.simple_preview.value}"
            )
        else:
            button = (
                f"[ {timestamp} ]"
                f"Purchased"
                f"    from {AddressDisplay(seller).short(3, 4)}"
                f"    + {action.simple_preview.value}"
            )
        button += f"• for {action.simple_preview.value}"

    return button

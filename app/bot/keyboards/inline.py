from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..keyboards import callback_data
from ..texts import buttons


def back() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=buttons.back, callback_data=callback_data.back)]
        ]
    )


def go_main() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=buttons.go_main, callback_data=callback_data.go_main)]
        ]
    )


def main(testnet: bool = False, api_key: bool = False) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        InlineKeyboardButton(
            text=buttons.switch_to_mainnet if testnet else buttons.switch_to_testnet,
            callback_data=callback_data.switch_to_mainnet if testnet else callback_data.switch_to_testnet,
        ),
        InlineKeyboardButton(
            text=buttons.set_api_key if not api_key else buttons.del_api_key,
            callback_data=callback_data.set_api_key if not api_key else callback_data.del_api_key,
        ),
        # InlineKeyboardButton(
        #     text=buttons.terms,
        #     url="https://tonviewer.com/terms",
        # ),
        # InlineKeyboardButton(
        #     text=buttons.privacy,
        #     url="https://tonviewer.com/privacy",
        # )
    )
    return markup


def api_key_invalid() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=buttons.del_api_key, callback_data=callback_data.del_api_key)]
        ]
    )


def information(account_id: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    markup.row(
        InlineKeyboardButton(
            text=buttons.transactions,
            switch_inline_query_current_chat=f"{callback_data.transactions} {account_id}",
        )
    )
    markup.add(
        InlineKeyboardButton(
            text=buttons.tokens,
            switch_inline_query_current_chat=f"{callback_data.tokens} {account_id}",
        ),
        InlineKeyboardButton(
            text=buttons.collectibles,
            switch_inline_query_current_chat=f"{callback_data.collectibles} {account_id}",
        ),
    )
    markup.row(
        InlineKeyboardButton(
            text=buttons.go_main,
            callback_data=callback_data.go_main,
        )
    )

    return markup


def information_jetton(account_id: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    markup.row(
        InlineKeyboardButton(
            text=buttons.transactions,
            switch_inline_query_current_chat=f"{callback_data.transactions} {account_id}",
        )
    )
    markup.add(
        InlineKeyboardButton(
            text=buttons.holders,
            switch_inline_query_current_chat=f"{callback_data.holders} {account_id}",
        ),
        InlineKeyboardButton(
            text=buttons.metadata,
            callback_data=callback_data.metadata,
        ),
    )
    markup.row(
        InlineKeyboardButton(
            text=buttons.go_main,
            callback_data=callback_data.go_main,
        )
    )

    return markup


def information_nft(account_id: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    markup.row(
        InlineKeyboardButton(
            text=buttons.transactions,
            switch_inline_query_current_chat=f"{callback_data.transactions} {account_id}",
        )
    )
    markup.add(
        InlineKeyboardButton(
            text=buttons.attributes,
            callback_data=callback_data.attributes,
        ),
        InlineKeyboardButton(
            text=buttons.metadata,
            callback_data=callback_data.metadata,
        ),
    )
    markup.row(
        InlineKeyboardButton(
            text=buttons.go_main,
            callback_data=callback_data.go_main,
        )
    )

    return markup


def information_collection(account_id: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    markup.row(
        InlineKeyboardButton(
            text=buttons.transactions,
            switch_inline_query_current_chat=f"{callback_data.transactions} {account_id}",
        )
    )
    markup.add(
        InlineKeyboardButton(
            text=buttons.items,
            switch_inline_query_current_chat=f"{callback_data.items} {account_id}",
        ),
        InlineKeyboardButton(
            text=buttons.metadata,
            callback_data=callback_data.metadata,
        ),
    )
    markup.row(
        InlineKeyboardButton(
            text=buttons.go_main,
            callback_data=callback_data.go_main,
        )
    )

    return markup

import calendar
import datetime
from dataclasses import dataclass

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..keyboards import callback_data
from ..texts import buttons


def back() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=buttons.back, callback_data=callback_data.back)]
        ]
    )


def back__confirm() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=buttons.back, callback_data=callback_data.back),
             InlineKeyboardButton(text=buttons.confirm, callback_data=callback_data.confirm)]
        ]
    )


def export_as__csv_json() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=buttons.export_as_csv, callback_data=callback_data.export_as_csv),
             InlineKeyboardButton(text=buttons.export_as_json, callback_data=callback_data.export_as_json)],
        ]
    )


def open_in_inline_mode__back(inline_query: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=buttons.open_in_inline_mode, switch_inline_query_current_chat=inline_query)],
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
    )
    return markup


def api_key_invalid() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=buttons.del_api_key, callback_data=callback_data.del_api_key)]
        ]
    )


def set_api_key() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=buttons.set_api_key, callback_data=callback_data.set_api_key)]
        ]
    )


def information(account_id: str, from_inline: bool = False) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    if not from_inline:
        markup.row(
            InlineKeyboardButton(
                text=buttons.events, callback_data=callback_data.events
            )
        )
    if from_inline:
        markup.row(
            InlineKeyboardButton(
                text=buttons.events, switch_inline_query_current_chat=f"{callback_data.events} {account_id}"
            )
        )
    markup.add(
        InlineKeyboardButton(
            text=buttons.tokens, switch_inline_query_current_chat=f"{callback_data.tokens} {account_id}",
        ),
        InlineKeyboardButton(
            text=buttons.collectibles, switch_inline_query_current_chat=f"{callback_data.collectibles} {account_id}",
        ),
    )
    if not from_inline:
        markup.row(
            InlineKeyboardButton(
                text=buttons.go_main, callback_data=callback_data.go_main,
            )
        )

    return markup


def information_jetton(account_id: str, from_inline: bool = False) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    markup.row(
        InlineKeyboardButton(
            text=buttons.events, switch_inline_query_current_chat=f"{callback_data.events} {account_id}",
        )
    )
    if not from_inline:
        markup.add(
            InlineKeyboardButton(
                text=buttons.holders, switch_inline_query_current_chat=f"{callback_data.holders} {account_id}",
            ),
            InlineKeyboardButton(
                text=buttons.metadata, callback_data=callback_data.metadata,
            ),
        )
        markup.row(
            InlineKeyboardButton(
                text=buttons.go_main, callback_data=callback_data.go_main,
            )
        )
    else:
        markup.add(
            InlineKeyboardButton(
                text=buttons.holders, switch_inline_query_current_chat=f"{callback_data.holders} {account_id}",
            )
        )

    return markup


def information_nft(account_id: str, from_inline: bool = False) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    markup.row(
        InlineKeyboardButton(
            text=buttons.events, switch_inline_query_current_chat=f"{callback_data.events} {account_id}",
        )
    )
    if not from_inline:
        markup.add(
            InlineKeyboardButton(
                text=buttons.attributes, callback_data=callback_data.attributes,
            ),
            InlineKeyboardButton(
                text=buttons.metadata, callback_data=callback_data.metadata,
            ),
        )
        markup.row(
            InlineKeyboardButton(
                text=buttons.go_main, callback_data=callback_data.go_main,
            )
        )

    return markup


def information_collection(account_id: str, from_inline: bool = False) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    if from_inline:
        markup.row(
            InlineKeyboardButton(
                text=buttons.events, switch_inline_query_current_chat=f"{callback_data.events} {account_id}",
            ),
        )
        markup.row(
            InlineKeyboardButton(
                text=buttons.items, switch_inline_query_current_chat=f"{callback_data.items} {account_id}",
            ),
        )
    else:
        markup.row(
            InlineKeyboardButton(
                text=buttons.events, switch_inline_query_current_chat=f"{callback_data.events} {account_id}",
            ),
        )
        markup.add(
            InlineKeyboardButton(
                text=buttons.items, switch_inline_query_current_chat=f"{callback_data.items} {account_id}",
            ),
            InlineKeyboardButton(
                text=buttons.metadata, callback_data=callback_data.metadata,
            ),
        )
        markup.row(
            InlineKeyboardButton(
                text=buttons.go_main, callback_data=callback_data.go_main,
            )
        )

    return markup


def information_event() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)

    markup.row(
        InlineKeyboardButton(
            text=buttons.show_json, callback_data=callback_data.show_json,
        )
    )
    markup.row(
        InlineKeyboardButton(
            text=buttons.back, callback_data=callback_data.back,
        )
    )

    return markup


@dataclass
class InlineKeyboardCalendar:
    back = "‹ Back"
    next = "Next ›"
    left = "‹"
    right = "›"

    cb_back = "cb_back"
    cb_next = "cb_next"
    cb_left = "cb_left"
    cb_right = "cb_right"

    cb_day = "cb_day"
    cb_month = "cb_month"
    cb_year = "cb_year"
    cb_blank = "_"

    selected = "· {} ·"
    selected_start_day = "› {} ·"
    selected_range_day = "› {} ‹"
    selected_end_day = "· {} ‹"

    export_for_all_time = "• Export for all time"
    cb_export_for_all_time = "cb_export_for_all_time"

    def __init__(self, date: int, start_date: int | None = None, end_date: int | None = None):
        self.date = datetime.datetime.fromtimestamp(date)
        self.start_date = datetime.datetime.fromtimestamp(start_date) if start_date else None
        self.end_date = datetime.datetime.fromtimestamp(end_date) if end_date else None

        self.months = {
            1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
            7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"
        }
        self.weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self.days = calendar.monthcalendar(self.date.year, self.date.month)

    def _years_inline_keyboard(self) -> list[list[InlineKeyboardButton]]:
        return [
            [
                InlineKeyboardButton(
                    text=self.left, callback_data=f"{self.cb_year}:{self.cb_left}"
                ),
                InlineKeyboardButton(
                    text=(
                        self.selected.format(self.date.year)
                        if (self.start_date and self.end_date and
                            self.start_date.year == self.end_date.year
                            ) and self.date.year == self.start_date.year
                        else self.date.year
                    ),
                    callback_data=self.cb_year,
                ),
                InlineKeyboardButton(
                    text=self.right, callback_data=f"{self.cb_year}:{self.cb_right}"
                ),
            ]
        ]

    def _months_inline_keyboard(self) -> list[list[InlineKeyboardButton]]:
        return [
            [
                InlineKeyboardButton(
                    text=self.left, callback_data=f"{self.cb_month}:{self.cb_left}"
                ),
                InlineKeyboardButton(
                    text=(
                        self.selected.format(self.months.get(self.date.month))
                        if (self.start_date and self.end_date and
                            self.start_date.month == self.end_date.month
                            ) and self.date.month == self.start_date.month
                        else self.months.get(self.date.month)
                    ),
                    callback_data=self.cb_month,
                ),
                InlineKeyboardButton(
                    text=self.right, callback_data=f"{self.cb_month}:{self.cb_right}"
                )
            ]
        ]

    def _week_inline_keyboard(self):
        return [
            [
                InlineKeyboardButton(text=week, callback_data=self.cb_blank) for week in self.weekdays
            ]
        ]

    def _days_inline_keyboard(self) -> list[list[InlineKeyboardButton]]:
        start_date_matches = (
            self.start_date.year == self.date.year and self.start_date.month == self.date.month
            if self.start_date else False
        )
        end_date_matches = (
            self.end_date.year == self.date.year and self.end_date.month == self.date.month
            if self.end_date else False
        )
        inline_keyboard = [
            [
                InlineKeyboardButton(
                    text=(
                        self.selected_range_day.format(day)
                        if (
                                   self.start_date and self.end_date and
                                   self.start_date.day == self.end_date.day
                           ) and self.start_date.day == day
                        else self.selected_start_day.format(day)
                        if start_date_matches and self.start_date.day == day
                        else self.selected_end_day.format(day)
                        if end_date_matches and self.end_date.day == day
                        else day if day != 0 else " "),
                    callback_data=f"{self.cb_day}:{day}" if day > 0 else self.cb_blank,
                ) for day in week
            ]
            for week in self.days
        ]

        return inline_keyboard

    def markup(self):
        markup = InlineKeyboardMarkup()

        markup.inline_keyboard += self._years_inline_keyboard()
        markup.inline_keyboard += self._months_inline_keyboard()
        markup.inline_keyboard += self._week_inline_keyboard()
        markup.inline_keyboard += self._days_inline_keyboard()

        markup.inline_keyboard += [
            [InlineKeyboardButton(text=self.export_for_all_time, callback_data=self.cb_export_for_all_time)]
        ]

        navigation_inline_keyboard = [InlineKeyboardButton(text=self.back, callback_data=self.cb_back)]
        if self.start_date and self.end_date:
            navigation_inline_keyboard.append(
                InlineKeyboardButton(text=self.next, callback_data=self.cb_next)
            )
        markup.inline_keyboard += [navigation_inline_keyboard]

        return markup


class InlineKeyboardPaginator:
    first_page_label = '« {}'
    previous_page_label = '‹ {}'
    current_page_label = '· {} ·'
    next_page_label = '{} ›'
    last_page_label = '{} »'

    def __init__(
            self,
            items: list[tuple],
            row_width: int = 1,
            total_pages: int = 1,
            current_page: int = 1,
            data_pattern='page:{}',
            after_buttons: list[list[InlineKeyboardButton]] = None,
            before_buttons: list[list[InlineKeyboardButton]] = None,
    ):
        self.items = items
        self.row_width = row_width
        self.total_pages = total_pages
        self.current_page = current_page
        self.data_pattern = data_pattern
        self.after_buttons = after_buttons
        self.before_buttons = before_buttons

    def _build_navigation(self) -> list[InlineKeyboardButton] | list[list]:
        keyboard_dict = {}

        if self.total_pages > 1:
            if self.total_pages <= 5:
                for page in range(1, self.total_pages + 1):
                    keyboard_dict[page] = page
            else:
                if self.current_page <= 3:
                    pages_range = range(1, 4)
                    keyboard_dict[4] = self.next_page_label.format(4)
                    keyboard_dict[self.total_pages] = self.last_page_label.format(self.total_pages)
                elif self.current_page > self.total_pages - 3:
                    keyboard_dict[1] = self.first_page_label.format(1)
                    keyboard_dict[self.total_pages - 3] = self.previous_page_label.format(self.total_pages - 3)
                    pages_range = range(self.total_pages - 2, self.total_pages + 1)
                else:
                    keyboard_dict[1] = self.first_page_label.format(1)
                    keyboard_dict[self.current_page - 1] = self.previous_page_label.format(self.current_page - 1)
                    keyboard_dict[self.current_page + 1] = self.next_page_label.format(self.current_page + 1)
                    keyboard_dict[self.total_pages] = self.last_page_label.format(self.total_pages)
                    pages_range = [self.current_page]
                for page in pages_range:
                    keyboard_dict[page] = page

            keyboard_dict[self.current_page] = self.current_page_label.format(self.current_page)
            return [[
                InlineKeyboardButton(text=str(value), callback_data=self.data_pattern.format(key))
                for key, value in sorted(keyboard_dict.items())
            ]]
        else:
            return [[]]

    def _build_items(self) -> list[list[InlineKeyboardButton]]:
        markup = InlineKeyboardMarkup(row_width=self.row_width)
        markup.add(
            *[
                InlineKeyboardButton(text=str(text), callback_data=str(cdata))
                for text, cdata in self.items
            ]
        )
        return markup.inline_keyboard

    @property
    def inline_keyboard(self) -> list[list[InlineKeyboardButton]]:
        markup = InlineKeyboardMarkup(row_width=self.row_width)

        if self.after_buttons: markup.inline_keyboard += self.after_buttons  # noqa:E701
        markup.inline_keyboard += self._build_items()
        markup.inline_keyboard += self._build_navigation()
        if self.before_buttons: markup.inline_keyboard += self.before_buttons  # noqa:E701

        return markup.inline_keyboard

    @property
    def markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(inline_keyboard=self.inline_keyboard)

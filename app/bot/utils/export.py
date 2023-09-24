import csv
import json
from dataclasses import dataclass, asdict, fields
from datetime import datetime
from io import BytesIO
from typing import Optional

import aiofiles
from aiocsv import AsyncDictWriter
from pytonapi.schema.events import AccountEvents


@dataclass
class EventRow:
    datetime: str
    event_id: str
    account_address: str
    account_name: Optional[str] = None
    action_type: Optional[str] = None
    description: Optional[str] = None
    value: Optional[str] = None
    comment: Optional[str] = None
    first_account_address: Optional[str] = None
    second_account_address: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class EventRows:
    rows: Optional[list[EventRow]] = None

    def to_dict(self) -> dict:
        return asdict(self)


class ExportManager:

    def __init__(self, events: AccountEvents) -> None:
        self.rows = []
        self.events = events
        self.buffer = BytesIO()

    def _create_rows(self) -> EventRows:
        """
        Create and populate the rows for the event table.

        Returns:
            EventRows: The populated EventRows object.
        """
        for event in self.events.events:
            row = EventRow(
                event_id=event.event_id,
                account_address=event.account.address.to_userfriendly(),
                account_name=event.account.name,
                datetime=datetime.fromtimestamp(event.timestamp).strftime("%d-%m-%Y %H:%M"),
                action_type=event.actions[0].simple_preview.name,
                description=event.actions[0].simple_preview.description,
                value=event.actions[0].simple_preview.value,
            )
            if event.actions[0].TonTransfer \
                    and event.actions[0].TonTransfer.comment \
                    and event.actions[0].TonTransfer.comment != '':
                row.comment = event.actions[0].TonTransfer.comment
            if event.actions[0].JettonTransfer \
                    and event.actions[0].JettonTransfer.comment \
                    and event.actions[0].JettonTransfer.comment != '':
                row.comment = event.actions[0].JettonTransfer.comment
            if len(event.actions[0].simple_preview.accounts) == 1:
                row.first_account_address = event.actions[0].simple_preview.accounts[0].address.to_userfriendly()
            if len(event.actions[0].simple_preview.accounts) == 2:
                row.second_account_address = event.actions[0].simple_preview.accounts[1].address.to_userfriendly()
            self.rows.append(row)

        return EventRows(rows=self.rows)

    async def save_as_json(self) -> bytes:
        """
        Save the data as a JSON file and return the file content as bytes.

        Returns:
            bytes: The content of the JSON file as bytes.
        """
        async with aiofiles.tempfile.NamedTemporaryFile("w+", suffix=".json", delete=True) as f:
            data = json.dumps(self._create_rows().to_dict(),
                              ensure_ascii=False,
                              indent=2)
            await f.write(data)
            await f.seek(0)
            self.buffer = f.buffer.read()

        return self.buffer

    async def save_as_csv(self):
        """
        Save the data as a CSV file.

        This function saves the data as a CSV file by performing the following steps:
        1. Create a named temporary file with the .csv extension.
        2. Set the fieldnames for the CSV file based on the EventRow fields.
        3. Create an AsyncDictWriter object with the file, fieldnames, and quoting options.
        4. Write the fieldnames to the CSV file.
        5. Write the rows of data to the CSV file.
        6. Seek to the beginning of the file.
        7. Read the file buffer and store it in the buffer attribute.

        Returns:
            bytes: The file buffer containing the saved CSV data.
        """
        async with aiofiles.tempfile.NamedTemporaryFile("w+", suffix=".csv", delete=True) as f:
            fieldnames = {field.name: field.name for field in fields(EventRow)}
            writer = AsyncDictWriter(f, fieldnames, restval="null", quoting=csv.QUOTE_ALL)
            await writer.writerow(fieldnames)
            await writer.writerows(self._create_rows().to_dict()["rows"])
            await f.seek(0)
            self.buffer = f.buffer.read()

        return self.buffer

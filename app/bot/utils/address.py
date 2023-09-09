from dataclasses import dataclass

from aiogram.utils.markdown import hlink
from pytonapi.schema.accounts import AccountAddress, Account


@dataclass
class AddressDisplay:

    def __init__(self, account: Account | AccountAddress) -> None:
        self.account = account
        self.name = account.name
        self.address = account.address.to_userfriendly()

    def title(self) -> str:
        return self.name or self.address

    def short(self, length: int = 6, end: int = 4) -> str:
        return self.name or f"{self.address[:length]}...{self.address[-end:]}"

    def link(self, base_url: str = None) -> str:
        url = base_url or "https://tonviewer.com/"
        return hlink(self.title(), url=url + self.address)

    def short_link(self, base_url: str = None) -> str:
        url = base_url or "https://tonviewer.com/"
        return hlink(self.short(), url=url + self.address)

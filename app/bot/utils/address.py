from dataclasses import dataclass

from aiogram.utils.markdown import hlink
from pytonapi.schema.accounts import AccountAddress, Account


@dataclass
class AddressDisplay:
    _scam = "[SCAM!]"

    def __init__(self, account: Account | AccountAddress) -> None:
        self.account = account
        self.name = account.name
        self.address = account.address.to_userfriendly()
        self.is_scam = account.is_scam or False

        if addr_book.get(self.address):
            self.name = addr_book.get(self.address)
        if self.address in scam_book:
            self.is_scam = True

    def title(self) -> str:
        account = self.name or self.address
        return f"{self._scam} {account}" if self.is_scam else account

    def short(self, length: int = 6, end: int = 4) -> str:
        account = self.name or f"{self.address[:length]}...{self.address[-end:]}"
        return f"{self._scam} {account}" if self.is_scam else account

    def link(self, base_url: str = None) -> str:
        url = base_url or "https://tonviewer.com/"
        account = hlink(self.title(), url=url + self.address)
        return f"{self._scam} {account}" if self.is_scam else account

    def short_link(self, base_url: str = None) -> str:
        url = base_url or "https://tonviewer.com/"
        account = hlink(self.short(), url=url + self.address)
        return f"{self._scam} {account}" if self.is_scam else account


addr_book = {
    "EQCA14o1-VWhS2efqoh_9M1b_A9DtKTuoqfmkn83AbJzwnPi": ".t.me DNS",
    "Ef_lZ1T4NCb2mwkme9h2rJfESCE0W34ma9lWp7-_uY3zXDvq": "Root DNS",
    "EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c": "Burn Address",
    "EQAuz15H1ZHrZ_psVrAra7HealMIVeFq0wguqlmFno1f3EJj": "Telegram Team",
    "EQBAjaOyi2wGWlk-EDkSabqqnF-MrrwMadnwqrurKpkla9nE": "Fragment Marketplace",
    "EQCMOXxD-f8LSWWbXQowKxqTr3zMY-X1wMTyWp3B-LR6s3Va": "Fragment Cold Storage",
    "EQAOQdwdw8kGftJCSFgOErM1mBjYPe4DBPq8-AhF6vr9si5N": "Anonymous Telegram Numbers",
    "EQCjk1hh952vWaE9bRguFkAhDAL5jj3xj9p0uPWrFBq_GEMS": "Getgems Marketplace",
    "EQBYTuYbLf8INxFtD8tQeNk5ZLy-nAX9ahQbG_yl1qQ-GEMS": "Getgems Sales",
    "EQDrLq-X6jKZNHAScgghh0h1iog3StK71zn8dcmrOj8jPWRA": "Disintar Marketplace",
    "EQCJTkhd1W2wztkVNp_dsKBpv2SIoUWoIyzI7mQrbSrj_NSh": "TON Diamonds",
}

scam_book = [
    "Ef83SoX0iL2bkzkK6Z9Q8kuOYVtrzh2my3pTiJTBfBV78Ton",
    "EQCMmytWnOEHdAEzPel9DBEn9jB7B6lq9jfsaF_Qa8FjNGmB",
    "EQBZXztyL09Mq3kxZO5jrKpu0F3ziXGqAFREfvqq72XoGJJY",
    "EQDAcWAcCT2sV6hUJ84aubUOebA4m9ZBXWZOooN66Y3RGlhy",
    "EQDzFIRXUINKQN9QY0uXwApBGvpDnhgKhMpMKyaCwDxDgzNi",
    "EQBg1QV_P1H9QDGqsRI9OPzkk000vPQ4d34sq3IMvbSlV7f9",
    "EQAFGP1nFA5j-zxUdmuJ0V1RvX-5ecS7pv4lM-URhilb8FdA",
    "EQAOuLEuA7Tuvfvzmi0BWFFq_2t5iC4cIOMcJyWPG5_xRsVn",
    "EQChLBUYFaZ4mLVEuaBFDXUBjEBwQ-deeMEFS5ZVcLGWI3L0",
    "EQAPwB9l6ACiwRUieFcZN-4S3J8oG9htE7o7bWMg5V8g_Rpa",
    "EQCNgCFZ6vBrHHMJvJopfjpBPPSRajlj3etvm-rFAWKb8vep",
]

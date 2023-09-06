from dataclasses import dataclass

from aiogram.utils.markdown import hlink


@dataclass
class GetgemsLink:
    base_url = 'https://getgems.io'

    @classmethod
    def nft(cls, name: str, address: str) -> str:
        url = f"{cls.base_url}/nft/{address}"
        return hlink(title=name, url=url)

    @classmethod
    def collection(cls, name: str, address: str) -> str:
        url = f"{cls.base_url}/collection/{address}"
        return hlink(title=name, url=url)

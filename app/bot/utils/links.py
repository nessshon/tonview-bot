from dataclasses import dataclass

from aiogram.utils.markdown import hlink


@dataclass
class GetgemsLink:
    base_url = 'https://getgems.io'

    @classmethod
    def nft(cls, name: str, address: str) -> str:
        """
        Generate a hyperlink to an NFT based on its name and address.

        Args:
            name (str): The name of the NFT.
            address (str): The address of the NFT.

        Returns:
            str: The hyperlink to the NFT.
        """
        url = f"{cls.base_url}/nft/{address}"
        return hlink(title=name, url=url)

    @classmethod
    def collection(cls, name: str, address: str) -> str:
        """
        Generates a hyperlink to a collection with the given name and address.

        Parameters:
            name (str): The name of the collection.
            address (str): The address of the collection.

        Returns:
            str: The hyperlink to the collection.
        """
        url = f"{cls.base_url}/collection/{address}"
        return hlink(title=name, url=url)

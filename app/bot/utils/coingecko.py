from __future__ import annotations

import asyncio
import json

import aiofiles
import aiohttp
from pydantic import BaseModel, Field

from ..data import BASE_DIR


class Coingecko:

    def __init__(self, filename: str = f"{BASE_DIR}/ton_price.json") -> None:
        self.filename = filename

    @staticmethod
    async def get_price() -> str | None:
        """
        Retrieves the price of "the-open-network" in USD from the Coingecko API.

        Returns:
            str | None: The price of "the-open-network" in USD as a string, or None if the request fails.
        """
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {'ids': "the-open-network", 'vs_currencies': "usd"}

        async with aiohttp.ClientSession() as session:
            response = await session.get(url, params=params)
            return await response.text() if response.status == 200 else None

    async def update_price(self) -> None:
        """
        Update the price by retrieving it from an external source and writing it to a file.
        """
        price = await self.get_price()
        if not price: return  # noqa:E701
        async with aiofiles.open(self.filename, "w+") as f:
            await f.write(price)

    async def run_updates(self, seconds: int = 10) -> None:
        """
        Run updates at regular intervals.

        Args:
            seconds (int): The number of seconds to wait between updates. Defaults to 10.
        """
        while True:
            await self.update_price()
            await asyncio.sleep(seconds)

    async def get(self) -> Currency:
        """
        Get the currency data from the specified file.
        """
        async with aiofiles.open(self.filename, "r") as f:
            return Currency(**json.loads(await f.read()))


class Price(BaseModel):
    usd: None | float | int


class Currency(BaseModel):
    ton: None | Price = Field(alias='the-open-network')

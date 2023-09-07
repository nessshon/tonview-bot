from __future__ import annotations

import asyncio
import time
from asyncio import Event, Lock
from contextlib import suppress
from types import TracebackType

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import Throttled

USERS_THROTTLED: list[int] = []

EMOJIS_HOURGLASS: tuple[str, str] = ("⏳", "⌛️")
EMOJIS_MAGNIFIER: tuple[str, str] = ("🔍", "🔎")


class ThrottlingContext:
    DEFAULT_INTERVAL = 3.0
    DEFAULT_INITIAL_SLEEP = 0.0

    def __init__(
            self,
            *,
            bot: Bot,
            state: FSMContext,
            chat_id: str | int,
            message_id: int | None,
            emojis: tuple[str, str] = EMOJIS_HOURGLASS,
            interval: float = DEFAULT_INTERVAL,
            initial_sleep: float = DEFAULT_INITIAL_SLEEP,
    ) -> None:
        self.chat_id = chat_id
        self.message_id = message_id
        self.emojis = emojis
        self.interval = interval
        self.initial_sleep = initial_sleep
        self.state = state
        self.bot = bot

        self._lock = Lock()
        self._close_event = Event()
        self._closed_event = Event()
        self._task: asyncio.Task[any] | None = None

    @property
    def running(self) -> bool:
        return bool(self._task)

    async def _wait(self, interval: float) -> None:
        with suppress(asyncio.TimeoutError):
            await asyncio.wait_for(self._close_event.wait(), interval)

    async def _worker(self) -> None:
        from ..utils.message import edit_or_send_message
        try:
            counter = 0
            await self._wait(self.initial_sleep)
            while not self._close_event.is_set():
                start = time.monotonic()

                await edit_or_send_message(
                    bot=self.bot, state=self.state,
                    chat_id=self.chat_id, message_id=self.message_id,
                    text=self.emojis[0] if counter % 2 == 0 else self.emojis[1],
                )
                counter += 1
                interval = self.interval - (time.monotonic() - start)
                await self._wait(interval)
        finally:
            self._closed_event.set()

    async def _run(self) -> None:
        async with self._lock:
            self._close_event.clear()
            self._closed_event.clear()
            if self.running:
                raise RuntimeError("Already running")
            self._task = asyncio.create_task(self._worker())

    async def _stop(self) -> None:
        async with self._lock:
            if not self.running:
                return
            if not self._close_event.is_set():
                self._close_event.set()
                await self._closed_event.wait()
            self._task = None

    async def __aenter__(self) -> ThrottlingContext:
        await self._run()
        USERS_THROTTLED.append(self.chat_id)
        return self

    async def __aexit__(
            self,
            exc_type: type[BaseException] | None,
            exc_value: BaseException | None,
            traceback: TracebackType | None,
    ) -> any:
        await self._stop()
        USERS_THROTTLED.remove(self.chat_id)


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(
            self,
            message_limit: float = .8,
            callback_limit: float = .3,
            key_prefix: str = "antiflood_",
    ):
        self.prefix = key_prefix
        self.message_limit = message_limit
        self.callback_limit = callback_limit
        super(ThrottlingMiddleware, self).__init__()

    # noinspection PyUnusedLocal
    async def on_process_message(self, message: Message, data: dict):
        dispatcher = Dispatcher.get_current()
        handler = current_handler.get()

        if message.from_user.id in USERS_THROTTLED:
            raise CancelHandler()

        if handler:
            limit = getattr(handler, "throttling_rate_limit", self.message_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.message_limit
            key = f"{self.prefix}_message"

        try:
            from ..utils.message import delete_message
            await dispatcher.throttle(key, rate=limit)
            await delete_message(message)
        except Throttled:
            raise CancelHandler()

    # noinspection PyUnusedLocal
    async def on_process_callback_query(self, call: CallbackQuery, data: dict):
        dispatcher = Dispatcher.get_current()
        handler = current_handler.get()

        if call.from_user.id in USERS_THROTTLED:
            raise CancelHandler()

        if handler:
            limit = getattr(handler, "throttling_rate_limit", self.callback_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")

        else:
            limit = self.message_limit
            key = f"{self.prefix}_callback"

        try:
            await dispatcher.throttle(key, rate=limit)
            await call.answer()
        except Throttled:
            raise CancelHandler()


def rate_limit(limit: float, key=None):
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator

import asyncio
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from aiogram import Bot, Dispatcher
from aiogram.types import AllowedUpdates
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils.exceptions import Unauthorized


async def on_startup(dp: Dispatcher) -> None:
    from .config import Config
    config: Config = dp.bot["config"]

    from .bot.utils.coingecko import Coingecko
    asyncio.create_task(
        Coingecko().run_updates()
    )

    from .db.database import Database
    db = Database(config.db)
    dp.bot["db"] = await db.init()
    logging.info("Database initialized.")

    from .bot import filters
    filters.setup(dp)

    from .bot import middlewares
    middlewares.setup(dp)

    from .bot import handlers
    handlers.errors.register(dp)

    handlers.commands.register(dp)
    await handlers.commands.setup(dp)

    handlers.messages.register(dp)
    handlers.callbacks.register(dp)
    handlers.inlines.register(dp)


async def on_shutdown(dp: Dispatcher) -> None:
    from .bot.handlers import commands
    await commands.delete(dp)

    from .db.database import Database
    db: Database = dp.bot["db"]
    await db.close()
    logging.warning("Database closed.")

    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Dispatcher storage closed.")

    session = await dp.bot.get_session()
    await session.close()
    logging.warning("Bot session closed.")


def init():
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # noqa
        handlers=[
            TimedRotatingFileHandler(
                filename=f"logs/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
                when="midnight",
                interval=1,
                backupCount=5
            ),
            logging.StreamHandler(),
        ]
    )

    from .config import load_config
    config = load_config()

    bot = Bot(token=config.bot.TOKEN, parse_mode="HTML")
    storage = RedisStorage2(host=config.redis.HOST,
                            port=config.redis.PORT,
                            db=config.redis.DB)
    dp = Dispatcher(bot=bot, storage=storage)
    bot["config"] = config

    try:
        executor.start_polling(
            dispatcher=dp,
            skip_updates=False,
            reset_webhook=True,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            allowed_updates=AllowedUpdates.all()
        )

    except Unauthorized:
        logging.error("Invalid bot token!")

    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    init()

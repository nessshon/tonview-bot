from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from environs import Env

BASE_DIR = Path(__file__).resolve().parent


@dataclass
class BotConfig:
    TOKEN: str
    DEV_ID: int


@dataclass
class RedisConfig:
    HOST: str
    PORT: int
    DB: int


@dataclass
class DatabaseConfig:
    HOST: str
    PORT: int
    NAME: str
    USER: str
    PASS: str


@dataclass
class TonapiConfig:
    KEY: str
    ENCRYPTION_KEY: str


@dataclass
class Config:
    bot: BotConfig
    redis: RedisConfig
    db: DatabaseConfig
    tonapi: TonapiConfig


def load_config() -> Config:
    env = Env()
    env.read_env()

    return Config(
        bot=BotConfig(
            TOKEN=env.str("BOT_TOKEN"),
            DEV_ID=env.int("DEV_ID"),
        ),
        redis=RedisConfig(
            HOST=env.str("REDIS_HOST"),
            PORT=env.int("REDIS_PORT"),
            DB=env.int("REDIS_DB"),
        ),
        db=DatabaseConfig(
            HOST=env.str("DB_HOST"),
            PORT=env.int("DB_PORT"),
            NAME=env.str("DB_NAME"),
            USER=env.str("DB_USER"),
            PASS=env.str("DB_PASS"),
        ),
        tonapi=TonapiConfig(
            KEY=env.str("TONAPI_KEY"),
            ENCRYPTION_KEY=env.str("ENCRYPTION_KEY"),
        )
    )

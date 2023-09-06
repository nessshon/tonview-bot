from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .userdata import UserDataMiddleware


def setup(dp: Dispatcher):
    dp.setup_middleware(ThrottlingMiddleware())
    dp.setup_middleware(UserDataMiddleware())

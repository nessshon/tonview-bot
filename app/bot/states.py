from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.dispatcher.filters.state import State as St


class State(StatesGroup):
    main = St()

    set_api_key = St()
    api_key_invalid = St()

    information = St()
    detail = St()

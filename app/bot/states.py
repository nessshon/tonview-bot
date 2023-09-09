from aiogram.dispatcher.filters.state import StatesGroup
from aiogram.dispatcher.filters.state import State as St


class State(StatesGroup):
    main = St()

    set_api_key = St()
    api_key_invalid = St()

    information = St()
    information_event = St()
    information_event_json = St()
    detail = St()
    select_date = St()
    confirm_export = St()

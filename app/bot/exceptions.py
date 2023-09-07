from aiogram.utils.exceptions import BadRequest


class BadRequestMessageIsTooLong(BadRequest):
    match = "Message_too_long"

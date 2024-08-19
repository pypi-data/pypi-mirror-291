"""
This file is responsible for the Birthday class - the one used to save records' birthdays.
"""

from datetime import datetime
from .field import Field
from .boterror import BotError
from .texts import Texts

FORMAT = "%d.%m.%Y"


class Birthday(Field):
    def __init__(self, value: str):
        try:
            super().__init__(value)
            self.__bd_date = datetime.strptime(value, FORMAT)
        except ValueError:
            raise BotError(Texts.errors.get(Texts.INVALID_DATE, ''))

    @property
    def bd_date(self) -> datetime:
        return self.__bd_date

    def __str__(self):
        return self.bd_date.strftime(FORMAT)
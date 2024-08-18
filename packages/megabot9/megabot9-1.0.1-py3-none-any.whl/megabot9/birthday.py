"""
This file is responsible for the Birthday class - the one used to save records' birthdays.
"""

from datetime import datetime
from .field import Field
from .boterror import BotError

FORMAT = "%d.%m.%Y"
UNFORMAT = "DD.MM.YYYY"


class Birthday(Field):
    def __init__(self, value: str):
        try:
            super().__init__(value)
            self.__bd_date = datetime.strptime(value, FORMAT)
        except ValueError:
            raise BotError(f"Invalid date format. Use {UNFORMAT}")

    @property
    def bd_date(self) -> datetime:
        return self.__bd_date

    def __str__(self):
        return self.bd_date.strftime(FORMAT)
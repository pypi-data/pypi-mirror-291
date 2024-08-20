"""
This file is responsible for the Phone class - the one used to save records' phones.
"""

from typing import TypedDict
import re
from .field import Field
from .texts import PHONE_PREFIX


class Phone(Field):
    min_phone_len = 9
    max_phone_len = 12
    full_len = 13


    def __init__(self, value: str):
        super().__init__(value)
        self.validate_phone()

    def validate_phone(self):
        trimmed = ''.join(re.findall(r"\d+", self.value))
        self.value = None
        if Phone.max_phone_len >= len(trimmed) >= Phone.min_phone_len:
            self.value = f"{PHONE_PREFIX[:(Phone.full_len - len(trimmed))]}{trimmed}"


class PhoneData(TypedDict):
    phone: Phone
    index: int

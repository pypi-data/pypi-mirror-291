"""
This file is responsible for the Phone class - the one used to save records' phones.
"""

from typing import TypedDict
import re
from .field import Field


class Phone(Field):
    phone_len = 10

    def __init__(self, value: str):
        super().__init__(value)
        self.validate_phone()

    def validate_phone(self):
        trimmed = ''.join(re.findall(r"\d+", self.value))
        self.value = None
        if len(trimmed) >= Phone.phone_len:
            self.value = f"+38{trimmed[len(trimmed) - Phone.phone_len:]}"


class PhoneData(TypedDict):
    phone: Phone
    index: int

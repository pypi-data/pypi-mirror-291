"""
This file is responsible for the email classese - those used when saving records' emails.
"""

import re
from typing import TypedDict
from .field import Field


class Email(Field):
    email_regex = re.compile(
            r"^(?=.{1,256}$)(?:(?!@)[\w&'*+._%-]+(?:(?<=\w)\.[\w&'*+._%-]+)*|(?:(?!\d+@)[\w&'*+._%-]+(?:(?<=\w)\.[\w&'*+._%-]+)*))@(?:(?!\d+)[\w&'*+._%-]+(?:(?<=\w)\.[\w&'*+._%-]+)*|(?:(?!\d+)[\w&'*+._%-]+(?:(?<=\w)\.[\w&'*+._%-]+)*))\.[a-zA-Z]{2,}$",
            re.IGNORECASE
        )
    def __init__(self, value: str):
        super().__init__(value)
        self.validate_email()

    def validate_email(self):
        if Email.email_regex.fullmatch(self.value):
            self.value = self.value.lower()
        else:
            self.value = None

class EmailData(TypedDict):
    email: Email
    index: int

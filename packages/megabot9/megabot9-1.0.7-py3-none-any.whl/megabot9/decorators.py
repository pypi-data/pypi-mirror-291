"""
This file is responsible for the decorators - one wrapping functions for error handling, another - for text output.
"""

from functools import wraps
from .boterror import BotError
from .texts import Texts


def input_error(func):
    @wraps(func)
    def inner(*args):
        try:
            return func(*args)
        except BotError as e:
            print(str(e))
        except KeyboardInterrupt:
            print(Texts.messages[Texts.CANCELLED])
        except Exception as e:
            print(Texts.errors[Texts.GENERIC_ERROR])

    return inner


def show_message(func):
    @wraps(func)
    def inner(*args):
        message = func(*args)
        if type(message) == str:
            message = message.rstrip()
            print(message)
        else:
            print(Texts.errors[Texts.GENERIC_ERROR])


    return inner

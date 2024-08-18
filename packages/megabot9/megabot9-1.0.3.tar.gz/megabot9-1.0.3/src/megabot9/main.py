"""
This file is the entry point of the full application. It also handles some special user input values.
"""

import os
from typing import Tuple
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from .handler import get_response, save_session
from .texts import Texts


def parse_input(user_input: str) -> Tuple:
    if not user_input:
        return Texts.INVALID_CMD

    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Texts.messages[Texts.WELCOME])
    advanced_mode = True
    try:
        bot_completer = WordCompleter(Texts.commands + [Texts.FIND + ' ' + find for find in Texts.finds], ignore_case=True, sentence=True)
        session = PromptSession(completer=bot_completer)
    except:
        advanced_mode = False
    while True:
        try:
            if advanced_mode:
                cmd, *args = parse_input(session.prompt(Texts.messages[Texts.ENTER_CMD]))
            else:
                cmd, *args = parse_input(input(Texts.messages[Texts.ENTER_CMD]))
        except KeyboardInterrupt:
            print(('' if advanced_mode else '\n') + Texts.messages[Texts.EXIT_KB])
            break
        except EOFError:
            print(Texts.messages[Texts.EXIT_KB])
            break
        if cmd in [Texts.CLOSE, Texts.EXIT]:
            save_session()
            print(Texts.messages[Texts.EXIT])
            break

        if cmd in Texts.commands:
            get_response(cmd, args)
        else:
            print(Texts.messages[Texts.INVALID_CMD])


if __name__ == "__main__":
    main()

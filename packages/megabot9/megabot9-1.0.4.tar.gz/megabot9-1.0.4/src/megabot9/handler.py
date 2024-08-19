"""
This file is responsible for the user input handling and data saving.
"""

from typing import List, Dict
from .texts import Texts
from .decorators import input_error, show_message
from .session_handler import save_data, load_data
from .address import AddressParams, Params
from .boterror import BotError
from .birthday import FORMAT
from . import utils

loaded_data = load_data()
address_book = loaded_data["address_book"]
note_book = loaded_data["note_book"]


def get_response(cmd: str, args: List):
    match cmd:
        case Texts.HELLO:
            say_hello()
        case Texts.ADD:
            add_contact(args)
        case Texts.CHANGE:
            change_contact(args)
        case Texts.DELETE:
            delete_contact(args)
        case Texts.PHONE:
            show_all_phones(args)
        case Texts.ALL:
            show_all_contacts()
        case Texts.ADD_BD:
            add_birthday(args)
        case Texts.SHOW_BD:
            show_birthday(args)
        case Texts.BD_SOON:
            birthdays(args)
        case Texts.ADD_ADR:
            add_address(args)
        case Texts.CHANGE_ADR:
            change_address(args)
        case Texts.ADD_NOTE:
            add_note()
        case Texts.CHANGE_NOTE:
            change_note(args)
        case Texts.DELETE_NOTE:
            delete_note(args)
        case Texts.SORT_NOTES:
            sort_notes(args)
        case Texts.SHOW_NOTES:
            show_notes()
        case Texts.FIND:
            find(args)
        case Texts.ADD_EMAIL:
            return add_email(args)
        case Texts.CHANGE_EMAIL:
            return change_email(args)
        case Texts.DELETE_EMAIL:
            return delete_email(args)
        case Texts.SHOW_EMAIL:
            return show_email(args)
        case Texts.HELP:
            return show_help(args)
        case Texts.SAVE:
            return save_session()


@show_message
def save_session():
    save_data({
        "address_book": address_book,
        "note_book": note_book
    })
    return Texts.messages.get(Texts.SESSION_SAVED, '')


@show_message
def say_hello() -> str:
    return Texts.messages.get(Texts.HELLO, '')


@input_error
@show_message
def add_contact(args: List[str]) -> str:
    if len(args) < 1: return Texts.messages.get(Texts.INVALID_CMD, '')
    name, *rest = args
    record = address_book.find_record(name)
    message = Texts.messages.get(Texts.CHANGE, '')
    if not record:
        address_book.add_record(name)
        message = Texts.messages.get(Texts.ADD, '')
    if rest:
        record = address_book.find_record(name)
        error = record.add_phone(rest[0])
        if error:
            message = error
    return message


@input_error
@show_message
def change_contact(args: List[str]) -> str:
    if len(args) < 3: return Texts.messages.get(Texts.INVALID_CMD, '')
    name, phone, new_phone = args[:3]
    record = address_book.find_record(name)
    message = Texts.errors.get(Texts.NOT_FOUND, '')
    if record:
        error = record.edit_phone(phone, new_phone)
        if not error:
            message = Texts.messages.get(Texts.CHANGE, '')
        else:
            message = error
    return message


@input_error
@show_message
def delete_contact(args: List[str]) -> str:
    if len(args) < 1: return Texts.messages.get(Texts.INVALID_CMD, '')
    name = args[0]
    record = address_book.find_record(name)
    message = Texts.errors.get(Texts.NOT_FOUND, '')
    if record:
        address_book.delete_record(name)
        message = Texts.messages.get(Texts.DELETE, '')
    return message


@input_error
@show_message
def show_all_phones(args: List[str]) -> str:
    if len(args) < 1: raise BotError(Texts.messages.get(Texts.INVALID_CMD, ''))
    name = args[0]
    record = address_book.find_record(name)
    message = Texts.errors.get(Texts.NOT_FOUND, '')
    if record:
        message = Texts.messages.get(Texts.PHONES_EMPTY, '')
        if record.phones:
            message = Texts.messages.get(Texts.PHONES_LIST, '').format(name)
            message += ', '.join(p.value for p in record.phones)
    return message


@input_error
@show_message
def show_all_contacts() -> str:
    message = Texts.errors.get(Texts.EMPTY, '')
    if not address_book: raise BotError(Texts.errors.get(Texts.EMPTY, ''))
    message = Texts.messages.get(Texts.CONTACTS_LIST, '').format(len(address_book))
    message += str(address_book)
    return message


@input_error
@show_message
def add_birthday(args: List[str]) -> str:
    if len(args) < 2: return Texts.messages.get(Texts.INVALID_CMD, '')
    name, birthday = args[:2]
    record = address_book.find_record(name)
    message = Texts.errors.get(Texts.NOT_FOUND, '')
    if record:
        record.add_birthday(birthday)
        message = Texts.messages.get(Texts.CHANGE, '')
    return message


@input_error
@show_message
def show_birthday(args: List[str]) -> str:
    if len(args) < 1: return Texts.messages.get(Texts.INVALID_CMD, '')
    name = args[0]
    record = address_book.find_record(name)
    message = Texts.errors.get(Texts.NOT_FOUND, '')
    if record:
        if record.birthday is None: return message
        message = record.birthday.bd_date.date()
    return message


@input_error
@show_message
def birthdays(args: List[str]) -> str:
    delta = None
    if len(args) >= 1:
        try:
            delta = int(args[0])
        except ValueError:
            raise BotError(Texts.errors.get(Texts.INVALID_NUMBER, ''))
        else:
            if delta < 0: raise BotError(Texts.errors.get(Texts.INVALID_NUMBER, ''))
    if not address_book: raise BotError(Texts.errors.get(Texts.EMPTY, ''))
    bd_entries = []
    for record in address_book.values():
        record_bd_now = utils.is_bd_in_range(record, delta)
        if record_bd_now:
            dates = utils.get_congrats_date(record_bd_now)
            entry = {
                "name": record.name,
                "congrats_date": dates[0],
                "birthday": dates[1]
            }
            bd_entries.append(entry)
    bd_entries.sort(key=lambda e: e["congrats_date"])

    if bd_entries:
        message = Texts.messages.get(Texts.BD_FOUND, '')
        for entry in bd_entries:
            entry["congrats_date"] = entry["congrats_date"].strftime(FORMAT)
            entry["birthday"] = entry["birthday"].strftime(FORMAT)
            if entry["congrats_date"] == entry["birthday"]:
                message += f"{entry["name"]}: {entry["congrats_date"]}\n"
            else:
                message += f"{entry["name"]}: {entry["congrats_date"]} (from {entry["birthday"]})\n"
    else:
        message = Texts.messages.get(Texts.BD_NOT_FOUND, '')

    return message


@input_error
@show_message
def add_address(args: List[str]) -> str:
    message = Texts.errors.get(Texts.NO_RECORD, '')
    if len(args) == 0:
        return message

    record = address_book.find_record(args[0])
    if not record:
        message = Texts.errors.get(Texts.NOT_FOUND, '')
        return message

    if record.address:
        message = Texts.errors.get(Texts.ADR_EXISTS, '')
        return message

    address_params = {
        Params.CITY: None,
        Params.STREET: None,
        Params.BUILDING: None
    }

    message = Texts.messages.get(Texts.ADD_ADR, '')
    while True:
        if address_params["city"] and address_params["street"] and address_params["building"]:
            record.update_address(address_params)
            break

        messages = get_messages(address_params)
        user_input = input(messages["message"])
        if user_input == Texts.QUIT:
            message = Texts.messages.get(Texts.QUIT_ADD_ADR, '')
            break

        if user_input:
            address_params[messages["param"]] = user_input
        else:
            print(messages["error"])
    return message


def get_messages(address_params: AddressParams) -> Dict:
    messages: Dict = {}
    if not address_params["city"]:
        messages["message"] = f"{Texts.messages.get(Texts.ADD_CITY, '')} ({Texts.messages.get(Texts.QUIT, '')}): "
        messages["error"] = Texts.errors.get(Texts.NO_CITY, '')
        messages["param"] = Params.CITY
    if address_params["city"] and not address_params["street"]:
        messages["message"] = f"{Texts.messages.get(Texts.ADD_STR, '')} ({Texts.messages.get(Texts.QUIT, '')}): "
        messages["error"] = Texts.errors.get(Texts.NO_STR, '')
        messages["param"] = Params.STREET
    if address_params["city"] and address_params["street"] and not address_params["building"]:
        messages["message"] = f"{Texts.messages.get(Texts.ADD_BLD, '')} ({Texts.messages.get(Texts.QUIT, '')}): "
        messages["error"] = Texts.errors.get(Texts.NO_BLD, '')
        messages["param"] = Params.BUILDING
    return messages


@input_error
@show_message
def change_address(args: List[str]) -> str:
    message = Texts.errors.get(Texts.NO_RECORD, '')
    if len(args) == 0:
        return message

    record = address_book.find_record(args[0])
    if not record:
        message = Texts.errors.get(Texts.NOT_FOUND, '')
        return message
    
    if not record.address:
        message = Texts.errors.get(Texts.NOT_FOUND, '')
        return message

    address_params: AddressParams = {
        Params.CITY: record.address.city,
        Params.STREET: record.address.street,
        Params.BUILDING: record.address.building
    }
    messages = {
        Params.CITY: Texts.messages.get(Texts.UPD_CITY, ''),
        Params.STREET: Texts.messages.get(Texts.UPD_STR, ''),
        Params.BUILDING: Texts.messages.get(Texts.UPD_BLD, ''),
    }

    message = Texts.messages.get(Texts.UPD_ADR, '')
    for param in address_params:
        user_input = input(f"{messages[param]} [{address_params[param]}] ({Texts.messages.get(Texts.QUIT, '')}, "
                           f"{Texts.messages.get(Texts.PROCEED, '')}): ")
        if user_input == Texts.QUIT:
            message = Texts.messages.get(Texts.QUIT_UPD_ADR, '')
            break

        if user_input:
            address_params[param] = user_input
            record.update_address(address_params)
    return message


@input_error
@show_message
def add_note() -> str:
    note_params = {"title": "", "text": "", "tags": []}
    messages = {
        "title": {
            "msg": f"{Texts.messages.get(Texts.ADD_TITLE, '')} ({Texts.messages.get(Texts.QUIT, '')}): ",
            "err": Texts.errors.get(Texts.NO_TITLE, ''),
            "type": "title"
        },
        "text": {
            "msg": f"{Texts.messages.get(Texts.ADD_TEXT, '')} ({Texts.messages.get(Texts.QUIT, '')}): ",
            "err": Texts.errors.get(Texts.NO_TEXT, ''),
            "type": "text"
        }
    }

    result = Texts.messages.get(Texts.ADD_NOTE, '')
    while True:
        if note_params["title"] and note_params["text"] and not note_book.find_note(note_params["title"]):
            tags_input = input(f"{Texts.messages.get(Texts.ADD_TAGS, '')} ({Texts.messages.get(Texts.QUIT, '' )}): ")
            note_params["tags"] = tags_input.split(",") if tags_input else []
            note_book.add_note(note_params)
            break

        message = messages["title"] if not note_params["title"] else messages["text"]
        user_input = input(message["msg"])
        if user_input == "q":
            result = Texts.messages.get(Texts.QUIT_ADD_NOTE, '')
            break

        if user_input:
            note_params[message["type"]] = user_input
        else:
            print(message["err"])
    return result


@input_error
@show_message
def change_note(args: List[str]) -> str:
    if len(args) == 0:
        raise BotError(Texts.errors.get(Texts.NO_ARGS, ''))

    note = note_book.find_note(args)
    if not note:
        raise BotError(Texts.errors.get(Texts.NOTE_NOT_FOUND, ''))

    note_params = {"title": note.title, "text": note, "tags": note.tags}
    messages = {
        "title": f"{Texts.messages.get(Texts.UPD_TITLE, '')} ({Texts.messages.get(Texts.QUIT, '')}, "
                 f"{Texts.messages.get(Texts.PROCEED, '')}): ",
        "text": f"{Texts.messages.get(Texts.UPD_TEXT, '')} ({Texts.messages.get(Texts.QUIT, '')}, "
                 f"{Texts.messages.get(Texts.PROCEED, '')}): ",
        "tags": f"{Texts.messages.get(Texts.UPD_TAGS, '')} ({Texts.messages.get(Texts.QUIT, '')}, "
                 f"{Texts.messages.get(Texts.PROCEED, '')}): ",
    }
    result = Texts.messages.get(Texts.CHANGE_NOTE, '')

    for param in note_params:
        user_input = input(messages[param])
        if user_input == "q":
            result = Texts.messages.get(Texts.QUIT_UPD_NOTE, '')
            break

        if user_input:
            note_params[param] = user_input

    note.update_note(note_params)
    return result


@show_message
def delete_note(args: List[str]) -> str:
    if len(args) == 0:
        raise BotError(Texts.errors.get(Texts.NO_ARGS, ''))

    message = Texts.errors.get(Texts.NOTE_NOT_FOUND, '')
    if len(args) > 0 and note_book.find_note(args):
        note_book.remove_note(args)
        message = Texts.messages.get(Texts.DELETE_NOTE, '')
    return message


@show_message
def sort_notes(args: List[str]) -> str:
    message = Texts.errors.get(Texts.NO_ARGS, '')
    if len(args) > 0:
        trimmed = [tag.strip().lower() for tag in args]
        if len(trimmed) > 0:
            notes = note_book.get_notes_by_tag(trimmed)
            if notes:
                message = "\n" + notes
            else:
                message = Texts.errors.get(Texts.NOTES_NOT_FOUND, '')
    return message


@show_message
def show_notes() -> str:
    message = Texts.errors.get(Texts.NOTES_EMPTY, '')
    if bool(note_book):
        message = str(note_book)
    return message


@input_error
@show_message
def find(args: List[str]) -> str:
    if len(args) < 2: raise BotError(Texts.messages.get(Texts.INVALID_CMD, ''))
    field = args[0].casefold()
    if field not in Texts.finds: raise BotError(Texts.messages.get(Texts.INVALID_CMD, ''))
    perfect_match = False
    if len(args) == 2:
        query = args[1]
        perfect_match = True
    elif len(args) > 2:
        like_keyword = args[1].casefold()
        query = ''.join(args[2:])
        if like_keyword != Texts.LIKE: raise BotError(Texts.messages.get(Texts.INVALID_CMD, ''))
    
    results = []
    for record in address_book.values():
        if record.find_match(field, query, perfect_match):
            results.append(record)
    message = Texts.messages.get(Texts.FIND_NONE, '')
    if results:
        message = Texts.messages.get(Texts.FIND_LIST, '').format(len(results))
        for record in results:
            message += f"{str(record)}\n"
    return message


@input_error
@show_message
def add_email(args: List[str]) -> str:
    if len(args) < 2:
        return Texts.messages.get(Texts.INVALID_CMD, '')
    name, email = args[:2]
    record = address_book.find_record(name)
    if not record:
        raise BotError(Texts.errors.get(Texts.NOT_FOUND, ''))
    error = record.add_email(email)
    if error:
        return error
    return Texts.messages.get(Texts.ADD_EMAIL, '')


@input_error
@show_message
def change_email(args: List[str]) -> str:
    if len(args) < 3:
        return Texts.messages.get(Texts.INVALID_CMD, '')
    name, old_email, new_email = args[:3]
    record = address_book.find_record(name)
    if not record:
        raise BotError(Texts.errors.get(Texts.NOT_FOUND, ''))
    error = record.update_email(old_email, new_email)
    if error:
        return error
    return Texts.messages.get(Texts.CHANGE_EMAIL, '')


@input_error
@show_message
def delete_email(args: List[str]) -> str:
    if len(args) < 2:
        return Texts.messages.get(Texts.INVALID_CMD, '')
    name, email = args[:2]
    record = address_book.find_record(name)
    if not record:
        raise BotError(Texts.errors.get(Texts.NOT_FOUND, ''))
    error = record.remove_email(email)
    if error:
        return error
    return Texts.messages.get(Texts.DELETE_EMAIL, '')


@input_error
@show_message
def show_email(args: List[str]) -> str:
    if len(args) < 1: raise BotError(Texts.messages.get(Texts.INVALID_CMD, ''))
    name = args[0]
    record = address_book.find_record(name)
    message = Texts.errors.get(Texts.NOT_FOUND, '')
    if record:
        message = Texts.messages.get(Texts.EMAILS_EMPTY, '')
        if record.emails:
            message = Texts.messages.get(Texts.EMAILS_LIST, '').format(name)
            message += ', '.join(e.value for e in record.emails)
    return message


@input_error
@show_message
def show_help(args: List[str]) -> str:
    command = None
    if len(args) >= 1:
        command = args[0].casefold()
        if command in Texts.commands and command in Texts.helps:
            help = Texts.helps[command]
            message = f"{command} - {help}\n"
            return message

    message = Texts.messages.get(Texts.HELP_MESSAGE, '')
    for cmd in Texts.commands:
        if cmd in Texts.helps:
            help = Texts.helps[cmd]
            message += f"{cmd} - {help}\n"
    return message
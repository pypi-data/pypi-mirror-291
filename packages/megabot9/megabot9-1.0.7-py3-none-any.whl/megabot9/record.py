"""
This file is responsible for the Record class - the one used to keep an individual record.
"""

import re
from .address import Address, AddressParams
from .name import Name
from .phone import Phone, PhoneData
from .email import Email, EmailData
from .texts import Texts
from .birthday import Birthday


class Record:
    def __init__(self, name: str):
        self.__name = Name(name)
        self.__phones = []
        self.__birthday = None
        self.__address = None
        self.__emails = []

    def __str__(self):
        contact_card = ""
        contact_card += Texts.messages.get(Texts.CONTACT_NAME, '') + (self.name.value if self.name else Texts.messages.get(Texts.UNDEFINED, ''))
        contact_card += Texts.messages.get(Texts.CONTACT_PHONES, '') + (', '.join(p.value for p in self.phones) if self.phones else Texts.messages.get(Texts.NONE_SAVED, ''))
        contact_card += Texts.messages.get(Texts.CONTACT_EMAILS, '') + (', '.join(e.value for e in self.emails) if self.emails else Texts.messages.get(Texts.NONE_SAVED, ''))
        contact_card += Texts.messages.get(Texts.CONTACT_ADDRESS, '') + (self.address.value if self.address else Texts.messages.get(Texts.NOT_SET, ''))
        contact_card += Texts.messages.get(Texts.CONTACT_BIRTHDAY, '') + (self.birthday.value if self.birthday else Texts.messages.get(Texts.NOT_SET, ''))
        contact_card += '\n'
        return contact_card

    @property
    def name(self):
        return self.__name

    @property
    def phones(self):
        return self.__phones
    
    @property
    def emails(self):
        return self.__emails

    @property
    def birthday(self):
        return self.__birthday

    @property
    def address(self):
        return self.__address

    def add_phone(self, phone: str) -> str:
        new_phone = Phone(phone)
        if not new_phone.value:
            return Texts.errors.get(Texts.INVALID_PHONE)

        if not self.find_phone(new_phone):
            self.__phones.append(new_phone)
        else:
            return Texts.errors.get(Texts.PHONE_EXISTS)

    def edit_phone(self, current: str, new: str) -> str:
        found_phone = self.find_phone(Phone(current))
        if not found_phone:
            return Texts.errors.get(Texts.PHONE_NOT_FOUND)

        new_phone = Phone(new)
        if found_phone["phone"].value == new_phone.value:
            return Texts.errors.get(Texts.PHONE_EXISTS)

        self.__phones[found_phone["index"]] = new_phone

    def remove_phone(self, phone: str) -> str:
        found_phone = self.find_phone(Phone(phone))
        if not found_phone:
            return Texts.errors.get(Texts.PHONE_NOT_FOUND)

        self.__phones.pop(found_phone["index"])

    def find_phone(self, phone: Phone) -> PhoneData:
        values = [p.value for p in self.__phones]
        found = None
        if phone.value in values:
            found = {
                "phone": phone,
                "index": values.index(phone.value)
            }
        return found
    
    def add_email(self, email: str) -> str:
        new_email = Email(email)
        if not new_email.value:
            return Texts.errors.get(Texts.INVALID_EMAIL)

        if not self.find_email(new_email):
            self.__emails.append(new_email)
        else:
            return Texts.errors.get(Texts.EMAIL_EXISTS)
         
    def update_email(self, current: str, new: str) -> str:
        found_email = self.find_email(Email(current))
        if not found_email:
            return Texts.errors.get(Texts.EMAIL_NOT_FOUND)

        new_email = Email(new)
    
        if new_email.value is None:
            return Texts.errors.get(Texts.INVALID_EMAIL)

        if found_email["email"].value == new_email.value:
            return Texts.errors.get(Texts.EMAIL_EXISTS)

        self.__emails[found_email["index"]] = new_email

    def remove_email(self, email: str) -> str:
        found_email = self.find_email(Email(email))
        if not found_email:
            return Texts.errors.get(Texts.EMAIL_NOT_FOUND)

        self.__emails.pop(found_email["index"])

    def find_email(self, email: Email) -> EmailData:
        values = [e.value for e in self.__emails]
        found = None
        if email.value in values:
            found = {
                "email": email,
                "index": values.index(email.value)
            }
        return found


    def add_birthday(self, date: str):
        self.__birthday = Birthday(date)

    def update_address(self, params: AddressParams):
        self.__address = Address(params)

    def find_match(self, field: str, query: str, perfect_match: bool) -> bool:
        query = query.casefold()
        query = re.escape(query)
        if perfect_match:
            if query[0] != "^": query = "^" + query
            if query[-1] != "$": query = query + "$"
        else:
            query = query.replace("%", ".*")
            query = query.replace("_", ".{1}")
        match field:
            case Texts.NAME:
                string = self.name.value.casefold()
                result = re.search(query, string)
                return bool(result)
            case Texts.PHONE:
                for phone in self.phones:
                    string = phone.value.casefold()
                    result = re.search(query, string)
                    if result: return True
            case Texts.BIRTHDAY:
                if self.birthday is not None:
                    string = str(self.birthday)
                    result = re.search(query, string)
                    return bool(result)
            case Texts.ADDRESS:
                if self.address is not None:
                    string = self.address.value.casefold()
                    result = re.search(query, string)
                    return bool(result)
            case Texts.CITY:
                if self.address is not None:
                    string = self.address.city.casefold()
                    result = re.search(query, string)
                    return bool(result)
            case Texts.STREET:
                if self.address is not None:
                    string = self.address.street.casefold()
                    result = re.search(query, string)
                    return bool(result)
            case Texts.BUILDING:
                if self.address is not None:
                    string = self.address.building.casefold()
                    result = re.search(query, string)
                    return bool(result)
            case Texts.EMAIL:
                for email in self.emails:
                    string = email.value
                    result = re.search(query, string)
                    if result: return True
        return False
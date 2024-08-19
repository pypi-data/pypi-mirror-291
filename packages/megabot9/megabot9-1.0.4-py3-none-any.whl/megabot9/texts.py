"""
This file is responsible for keeping all of the plain texts used in the app.
"""

DATE_FORMAT = "DD.MM.YYYY"
PHONE_PREFIX = "+380"

class Texts:
    ADD = "add"
    CHANGE = "change"
    DELETE = "delete"
    PHONE = "phone"
    ALL = "all"
    ADD_BD = "add-birthday"
    SHOW_BD = "show-birthday"
    ADD_NOTE = "add-note"
    CHANGE_NOTE = "change-note"
    DELETE_NOTE = "delete-note"
    SHOW_NOTES = "show-notes"
    ADD_ADR = "add-address"
    UPD_ADR = "upd-address"
    CHANGE_ADR = "change-address"
    BD_SOON = "birthdays"
    BD_FOUND = "bd-found"
    BD_NOT_FOUND = "bd-not-found"
    HELLO = "hello"
    CLOSE = "close"
    EXIT = "exit"
    GENERIC_ERROR = 'error'
    HELP = "help"

    WELCOME = "welcome"
    ENTER_CMD = "enter-command"
    CANCELLED = "cancelled"
    CONTACTS_LIST = "contacts-list"
    PHONES_LIST = "phones-list"
    PHONES_EMPTY = "phones-empty"
    EMAILS_LIST = "emails-list"
    EMAILS_EMPTY = "email-empty"
    FIND_LIST = "find-list"
    FIND_NONE = "find-none"
    HELP_MESSAGE = "help-message"
    ADD_TITLE = "enter-title"
    ADD_TEXT = "enter-text"
    ADD_TAGS = "enter-tags"
    UPD_TITLE = "update-title"
    UPD_TEXT = "update-text"
    UPD_TAGS = "update-tags"
    SORT_NOTES = "sort-notes"
    EMPTY = "empty"
    NOT_FOUND = "not-found"
    PHONE_NOT_FOUND = "phone-not-found"
    PHONE_EXISTS = "phone-exists"
    EXIT_KB = "exit-kb"
    INVALID_CMD = "invalid-command"
    INVALID_PHONE = "invalid-phone"
    INVALID_NUMBER = "invalid-number"
    INVALID_DATE = "invalid-date"
    NO_RECORD = "no-record"
    ADD_CITY = "enter-city"
    UPD_CITY = "update-city"
    NO_CITY = "no-city"
    ADD_STR = "enter-street"
    UPD_STR = "update-street"
    NO_STR = "no-street"
    ADD_BLD = "enter-building"
    UPD_BLD = "update-building"
    NO_BLD = "no-building"
    ADR_EXISTS = "address-exists"
    QUIT = "q"
    QUIT_ADD_ADR = "quit-adding-address"
    QUIT_UPD_ADR = "quit-updating-address"
    QUIT_ADD_NOTE = "quit-adding-note"
    QUIT_UPD_NOTE = "quit-updating-note"
    PROCEED = "proceed"
    NO_TITLE = "no-title"
    NO_TEXT = "no-text"
    NOTE_EXISTS = "note-exists"
    NOTE_NOT_FOUND = "note-not-found"
    NOTES_NOT_FOUND = "notes-not-found"
    NOTES_EMPTY = "notes-empty"
    NO_ARGS = "not-enough-args"

    FIND = "find"
    LIKE = "like"
    NAME = "name"
    BIRTHDAY = "birthday"
    ADDRESS = "address"
    CITY = "city"
    STREET = "street"
    BUILDING = "building"
    EMAIL = "email"

    ADD_EMAIL = "add-email"
    CHANGE_EMAIL = "change-email"
    DELETE_EMAIL = "delete-email"
    SHOW_EMAIL = "show-email"

    EMAIL_EXISTS = "email-exists"
    EMAIL_NOT_FOUND = "email-not-found"
    INVALID_EMAIL = "invalid-email"

    UNDEFINED = "undefined"
    NONE_SAVED = "none-saved"
    NOT_SET = "not-set"
    NONE = "none"

    CONTACT_NAME = "contact-name"
    CONTACT_PHONES = "contact-phones"
    CONTACT_EMAILS = "contact-emails"
    CONTACT_ADDRESS = "contact-address"
    CONTACT_BIRTHDAY = "contact-birthday"

    SAVE = "save"
    SESSION_SAVED = "session_saved"


    finds = (NAME, PHONE, EMAIL, ADDRESS, CITY, STREET, BUILDING, BIRTHDAY)

    commands = [
        ADD,
        PHONE,
        CHANGE,
        ADD_EMAIL,
        SHOW_EMAIL,
        CHANGE_EMAIL,
        ADD_ADR,
        CHANGE_ADR,
        ADD_BD,
        SHOW_BD,

        ALL,
        FIND,
        
        DELETE,
        DELETE_EMAIL,

        BD_SOON,

        ADD_NOTE,
        SHOW_NOTES,
        CHANGE_NOTE,
        SORT_NOTES,
        DELETE_NOTE,
        
        HELLO,
        SAVE,
        HELP,
        CLOSE,
        EXIT,
    ]

    helps = {
        HELLO: "Show greeting",
        ADD: "Add a contact or add a phone to a contact",
        CHANGE: "Change a contact's phone",
        DELETE: "Delete a contact by name",
        PHONE: "Show a contact's phone number(s)",
        ALL: "Show all contacts in the address book with their data",
        ADD_BD: f"Add a birthday to a contact - in {DATE_FORMAT} form",
        SHOW_BD: f"Show contact's birthday, if present, in {DATE_FORMAT} form",
        BD_SOON: "Show birthdays in the upcoming week, or in N upcoming days",
        ADD_ADR: "Add address data to a contact",
        CHANGE_ADR: "Change address data of a contact",
        ADD_NOTE: "Add a note",
        CHANGE_NOTE: "Change a note",
        DELETE_NOTE: "Delete a note",
        SORT_NOTES: "Filter notes by tags",
        SHOW_NOTES: "Show all notes",
        FIND: "Search for contacts",
        ADD_EMAIL: "Add an email address to a contact",
        CHANGE_EMAIL: "Change a contact's email address",
        DELETE_EMAIL: "Delete a contact's email address",
        SHOW_EMAIL: "Show a contact's email address",
        SAVE: "Save the current state of the session", 
        HELP: "Show this help message",
        EXIT: "Exit the application" # CLOSE?
    }

    messages = {
        WELCOME: "Welcome to the assistant bot! [type help for help]",
        ENTER_CMD: "\nEnter a command: ",
        CANCELLED: "\nCancelled",
        CONTACTS_LIST: "Full contact list ({}):\n\n",
        PHONES_LIST: "Full phone list of {}:\n\n",
        PHONES_EMPTY: "No phones found.",
        EMAILS_LIST: "Full email list of {}:\n\n",
        EMAILS_EMPTY: "No emails found.",
        FIND_LIST: "All contacts satisfying the query ({}):\n\n",
        FIND_NONE: "No contacts satisfying the query found.",
        HELP_MESSAGE: "List of commands:\n\n",
        ADD_TITLE: "Enter note title",
        ADD_TEXT: "Enter note text",
        ADD_TAGS: "Add note tags, comma separated (optional)",
        UPD_TITLE: "Update note title",
        UPD_TEXT: "Update note text",
        UPD_TAGS: "Update note tags, comma separated",
        QUIT_ADD_NOTE: "Quit adding note.",
        QUIT_UPD_NOTE: "Quit updating note.",
        HELLO: "How can I help you? [type help for help]",
        ADD: "Record added successfully.",
        CHANGE: "Record updated successfully.",
        DELETE: "Record deleted successfully.",
        ADD_NOTE: "Note added successfully.",
        CHANGE_NOTE: "Note updated successfully.",
        DELETE_NOTE: "Note deleted successfully.",
        EXIT: "Good bye!",
        EXIT_KB: "Good bye! [session not saved]",
        SESSION_SAVED: "[session saved]",
        INVALID_CMD: "Invalid command.",
        ADD_CITY: "Enter city",
        ADD_STR: "Enter street",
        ADD_BLD: "Enter building",
        ADD_ADR: "Address added successfully.",
        UPD_ADR: "Address updated successfully.",
        QUIT: "'q' to quit",
        QUIT_ADD_ADR: "Quit adding address.",
        QUIT_UPD_ADR: "Quit updating address.",
        PROCEED: "'enter' to proceed",
        UPD_CITY: "Update city name",
        UPD_STR: "Update street name",
        UPD_BLD: "Update building number",
        ADD_EMAIL: "Email added successfully.",
        CHANGE_EMAIL: "Email updated successfully.",
        DELETE_EMAIL: "Email deleted successfully.",
        INVALID_EMAIL: "Invalid email address format.",
        BD_FOUND: "The following birthdays found:\n\n",
        BD_NOT_FOUND: "No upcoming birthdays found.",
        CONTACT_NAME: "┌ Name: ",
        CONTACT_PHONES: "\n├ Phones: ",
        CONTACT_EMAILS: "\n├ Emails: ",
        CONTACT_ADDRESS: "\n├ Address: ",
        CONTACT_BIRTHDAY: "\n└ Birthday: ",
        UNDEFINED: "undefined",
        NONE_SAVED: "none saved",
        NOT_SET: "not set",
        NONE: "none",

    }

    errors = {
        NOT_FOUND: "Record was not found.",
        EMPTY: "Address book is empty.",
        INVALID_PHONE: "Invalid phone format.",
        INVALID_NUMBER: "Invalid number argument.",
        INVALID_DATE: f"Invalid date format. Use {DATE_FORMAT}",
        PHONE_EXISTS: "Phone already exists.",
        PHONE_NOT_FOUND: "Phone was not found.",
        NO_TITLE: "Note title is required.",
        NO_TEXT: "Note text is required.",
        NOTE_EXISTS: "Note already exists.",
        NOTE_NOT_FOUND: "Note was not found.",
        NOTES_NOT_FOUND: "No notes with provided tags.",
        NOTES_EMPTY: "Note book is empty.",
        NO_RECORD: "Record name is required.",
        NO_CITY: "City name is required.",
        NO_STR: "Street name is required.",
        NO_BLD: "Building number is required.",
        ADR_EXISTS: "Address already exists.",
        NO_ARGS: "Not enough arguments.",
        EMAIL_EXISTS: "Email already exists.",
        EMAIL_NOT_FOUND: "Email was not found.",
        INVALID_EMAIL: "Invalid email format.",
        GENERIC_ERROR: "An error happened.",
    }

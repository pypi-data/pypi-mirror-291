"""
This file is responsible for the NoteBook class, which is holding all the notes.
"""

from collections import UserDict
from typing import List
from .note import Note, NoteParams


class NoteBook(UserDict):
    def add_note(self, params: NoteParams) -> Note:
        note = Note(params["title"], params["text"])
        self[params["title"].lower()] = note
        if len(params["tags"]) > 0:
            note.add_tags(params["tags"])
        return note

    def remove_note(self, args: List[str]):
        title = " ".join(args).lower() if len(args) > 1 else args[0].lower()
        self.pop(title)

    def find_note(self, args: List[str]) -> Note:
        title = " ".join(args).lower() if len(args) > 1 else args[0].lower()
        note = None
        key = title.lower()
        if key in self:
            note = self[key]
        return note

    def get_notes_by_tag(self, tags: List[str]) -> str:
        notes = ""
        for title in self:
            common_items = [tag for tag in tags if tag in self[title].tags]
            if len(common_items) > 0:
                notes += f"{self[title]}\n\n"
        return notes

    def __str__(self):
        notes = "\n"
        for note in self:
            notes += f"{self[note]}\n\n"
        return notes

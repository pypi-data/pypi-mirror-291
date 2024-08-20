"""
This file is responsible for the note classes - those used to keep an individual note.
"""

from typing import List, TypedDict
from .field import Field
from .texts import Texts


class NoteParams(TypedDict):
    title: str
    text: str
    tags: List[str]


class Note(Field):
    def __init__(self, title: str, value: str):
        super().__init__(value)
        self.__title: str = title
        self.__tags: List[str] = []

    @property
    def title(self):
        return self.__title

    @property
    def tags(self):
        return self.__tags

    def add_tags(self, tags: List[str]):
        if len(tags) > 0:
            trimmed = [tag.strip().lower() for tag in tags]
            self.__tags.extend(list(set(trimmed)))

    def update_note(self, params: NoteParams):
        self.__title = params["title"]
        self.value = params["text"]
        self.add_tags(params["tags"])

    def __str__(self):
        return (
            f"{self.__title}\n"
            f"{self.value}\n"
            f"tags: {", ".join(self.__tags) if len(self.__tags) > 0 else Texts.messages.get(Texts.NONE, '')}"
        )

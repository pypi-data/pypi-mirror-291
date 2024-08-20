"""
This file is responsible for the Field class - the one used as the basis for all the data classes.
"""

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
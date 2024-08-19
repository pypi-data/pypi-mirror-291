"""A class for storing a contact's birthday."""

from datetime import datetime

from classes.field import Field

from handlers.validations import (
    input_birthday_validation,
)


class Birthday(Field):
    """
    A class for storing a contact's birthday.

    Inherits from Field. Validates that the birthday is in the format DD.MM.YYYY and
    converts the string representation to a datetime object.

    Method:
        __init__(self, value: str) - Initializes the birthday with a validated date.
    """

    def __init__(self, value: str):

        if input_birthday_validation(value):
            try:
                birthday = datetime.strptime(value, "%d.%m.%Y")
                super().__init__(birthday)
            except ValueError as exc:
                raise ValueError("Invalid date format. Use DD.MM.YYYY") from exc
        else:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return f'{self.value.strftime("%d.%m.%Y")}'

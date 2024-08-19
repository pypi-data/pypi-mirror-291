"""A base class for fields in a record."""


class Field:
    """
    A base class for fields in a record.

    Attributes:
        * value (str): The value of the field.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

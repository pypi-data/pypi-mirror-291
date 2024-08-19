from classes.field import Field


class Name(Field):
    """
    A class for storing a contact's name.
    Inherits from Field.
    """

    def __init__(self, name):
        super().__init__(name)
        self.value = name

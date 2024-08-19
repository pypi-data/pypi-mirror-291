"""Address class"""

from classes.field import Field


class Address(Field):
    """Address class"""

    def __init__(self, address):
        super().__init__(address)
        self.value = address

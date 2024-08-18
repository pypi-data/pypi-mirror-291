"""Email class"""

from classes.field import Field


class Email(Field):
    """Email class"""

    def __init__(self, email):
        super().__init__(email)
        self.value = email

"""Phone class"""

from classes.field import Field

from handlers.validations import (
    input_number_validation,
)


class Phone(Field):
    """Phone class"""

    def __init__(self, number):
        super().__init__(number)
        self.value = self.validate_number(number)

    def validate_number(self, number):
        """validates a phone number

        Args:
            number (int): phone number for validation

        Raises:
            ValueError: The phone number must contain 10 digits
            ValueError: The phone number must contain only numbers

        Returns:
            int: validated number
        """
        if input_number_validation(number) is False:
            raise ValueError(
                "The phone number must contain only "
                "numbers and lenth must contain 10 digits"
            )
        return number

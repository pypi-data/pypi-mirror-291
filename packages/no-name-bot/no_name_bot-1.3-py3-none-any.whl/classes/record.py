"""Record class"""

from datetime import datetime
from classes.birthday import Birthday
from classes.name import Name
from classes.phone import Phone
from classes.email import Email
from classes.address import Address


class Record:
    """
    A class for storing contact information, including name and phone numbers.

    Attributes:
        * name (Name) - The contact's name.
        * phones (list of Phone) - A list of the contact's phone numbers.
    """

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None

    def __str__(self):
        contact_string = f"Contact name: {self.name.value}"
        if len(self.phones) > 0:
            contact_string += f", phones: {', '.join(p.value for p in self.phones)}"

        if self.birthday:
            contact_string += f", birthday: {self.birthday}"

        if self.email:
            contact_string += f", email: {self.email}"

        if self.address:
            contact_string += f", address: {self.address}"

        return contact_string

    def add_phone(self, number: str):
        """
        Add a phone number to the record.

        Args:
            * phone (str) - The phone number to be added.
        """
        self.phones.append(Phone(number))

    def remove_phone(self, number: str):
        """
        Remove a phone number from the record.

        Args:
            * phone (str) - The phone number to be removed.
        """

        for phone in self.phones:
            if str(phone.value) == number:
                self.phones.remove(phone)

    def edit_phone(self, old_number: str, new_number: str):
        """
        Edit a phone number in the record.

        Args:
            * old_phone (str) - The phone number to be replaced.
            * new_phone (str) - The new phone number to replace the old one.
        """

        self.phones = list(
            map(
                lambda phone: Phone(new_number) if phone.value == old_number else phone,
                self.phones,
            )
        )

    def find_phone(self, number):
        """
        Find a phone number in the record.

        Args:
            * phone (str) - The phone number to find.

        Returns:
            * Phone - The phone object if found, None otherwise.
        """

        for phone in self.phones:
            if phone.value == number:
                return phone

    def add_birthday(self, date_of_birthday):
        """Add a birthday to the record."""
        self.birthday = Birthday(date_of_birthday)

    def add_email(self, email):
        """Add an email to the record."""
        self.email = Email(email)

    def add_address(self, address_string):
        """Add an address to the record."""
        self.address = Address(address_string)

    def edit_name(self, new_name):
        """Edit name in the record."""
        self.name.value = new_name

    def edit_email(self, new_email):
        """Edit email in the record."""
        if self.email is None:
            self.email = Email(new_email)
        self.email.value = new_email

    def edit_address(self, new_address):
        """Edit address in the record."""
        if self.address is None:
            self.address = Address(new_address)
        self.address.value = new_address

    def edit_birthday(self, new_birthday):
        """Edit birthday in the record."""
        if self.birthday is None:
            self.add_birthday(new_birthday)
        self.birthday.value = datetime.strptime(new_birthday, "%d.%m.%Y")

    def remove_email(self):
        """Delete email in the record."""
        self.email = None

    def remove_address(self):
        """Delete address in the record."""
        self.address = None

    def remove_birthday(self):
        """Delete birthday in the record."""
        self.birthday = None

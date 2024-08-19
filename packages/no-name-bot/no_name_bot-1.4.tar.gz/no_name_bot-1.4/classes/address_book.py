"""class AddressBook"""

from collections import UserDict
from datetime import datetime, timedelta


class AddressBook(UserDict):
    """
    Stores the contact book and methods for working with it.
    Inherits from UserDict.
    """

    def __str__(self):
        lines = [str(record) for record in self.data.values()]
        return "\n".join(lines)

    def add_record(self, record):
        """
        Add a contact record to the address book.

        Args:
            * record (Record) - The contact record to be added.
        """
        if record.name.value in self.data:
            raise KeyError(f"Record with name '{record.name.value}' already exists.")
        self.data[record.name.value] = record

    def find(self, name):
        """
        Finds a record by name.

        Args:
            * name(str) - The name of the contact to find.

        Returns:
            * Record - The contact record if found
        """
        record = self.data.get(name, None)
        return record

    def find_email(self, email):
        """
        Finds a record by email.

        Args:
            * email(str) - The email of the contact to find.

        Returns:
            * Record - The contact record if found
        """
        return next(
            (
                record
                for record in self.data.values()
                if record.email and record.email.value == email
            ),
            None,
        )

    def delete(self, name):
        """
        Deletes a record by name.

        Args:
            * name(str) - The name of the record to be deleted.
        """
        if name not in self.data:
            raise KeyError(f"Record with name '{name}' not found.")
        del self.data[name]

    def get_upcoming_birthdays(self, days):
        """
        Creates a list of contacts to wish happy birthday within the next 'days' days.

        Args:
            days (int): The number of days from today to check for upcoming birthdays.

        Returns:
            list: List of dicts containing contacts with upcoming birthdays.
        """
        today_datetime = datetime.today().date()
        upcoming_birthdays = []

        for name, record in self.data.items():
            if record.birthday:
                user_birthday = datetime.strptime(
                    str(record.birthday), "%d.%m.%Y"
                ).date()
                birthday_prepared = user_birthday.replace(year=today_datetime.year)
                if birthday_prepared < today_datetime:
                    birthday_prepared = birthday_prepared.replace(
                        year=today_datetime.year + 1
                    )

                if (birthday_prepared - today_datetime).days > days:
                    continue

                if birthday_prepared.weekday() > 5:
                    birthday_prepared += timedelta(days=7 - birthday_prepared.weekday())

                congratulation_date_str = birthday_prepared.strftime("%d.%m.%Y")
                upcoming_birthdays.append(
                    {"name": name, "congratulation_date": congratulation_date_str}
                )

        return upcoming_birthdays

    def find_by_phone(self, phone):
        """
        Finds a record by phone number.
        Args:
        * phone(str) - The phone number to search for.
        Returns:
        * dict - The record with the matching phone number.
        """
        return next(
            (
                record
                for record in self.data.values()
                for p in record.phones
                if p.value == phone
            ),
            None,
        )

"""birthday handlers"""

from helpers.assistant_info import table_show

from classes import AddressBook

from .decorators import input_error


@input_error
def add_birthday_to_contact(args, book: AddressBook):
    """Adds a birthday to the contact.

    Args:
        args (list): contains name and birthday
        book (class): contact list

    Returns:
        str: message that the birthday has been added to contact
    """
    name, date, *_ = args
    record = book.find(name)
    if record:
        record.add_birthday(date)
        return "Birthday added"
    else:
        return f"There is no contact {name}"


@input_error
def show_birthday(args, book: AddressBook):
    """Shows a birthday of the contact.

    Args:
        args (list): contains name
        book (class): contact list

    Returns:
        str: message that shows contact name and birthday
    """
    name, *_ = args
    record = book.find(name)
    if record:
        if not record.birthday:
            return f"There is no birthday for contact {name}"
        return f"{name} birthday: {record.birthday}"

    else:
        return f"There is no contact {name}"


@input_error
def show_upcoming_birthdays(book: AddressBook):
    """Shows all contacts with congratulations dates for the next X days.

    Args:
        book (AddressBook): contact list.

    Returns:
        str: message with a list of contacts with congratulations dates.
    """
    try:
        days = int(
            input(
                "Enter the number of days from today to check for upcoming birthdays: "
            ).strip()
        )
    except ValueError:
        return "Invalid input! Please enter a valid number of days."

    upcoming_birthdays = book.get_upcoming_birthdays(days)

    if len(upcoming_birthdays) == 0:
        return "No contacts that need to be congratulated within the specified period."

    headers = ["Name", "Congratulation date"]
    table_data = [
        [key["name"], key["congratulation_date"]] for key in upcoming_birthdays
    ]
    return table_show(headers, table_data)

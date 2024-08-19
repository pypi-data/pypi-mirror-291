"""A module for working with a list of contacts:
adding, editing, outputting, deleting."""

from helpers.assistant_info import table_show

from classes import AddressBook, Record

from .decorators import empty_contact_list, input_error


@input_error
def add_contact(name, book: AddressBook):
    """Adds a new contact to the contact list.

    Args:
        args (list): contains name and phone number
        book (class): contact list

    Returns:
        str: message that the contact has been added or updated
    """
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    return message


@empty_contact_list
@input_error
def change_contact(args, book: AddressBook):
    """Changes a contact's phone number by the name

    #     Args:
    #         args (list): contains name, old phone number and new phone number
    #         book (class): contact list

    #     Returns:
    #         str: notification that the contact has been changed, or contact not found
    #"""
    name, old_number, new_number, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"No such name '{name}' was found")
    record.edit_phone(old_number, new_number)
    return "Phone changed"


@empty_contact_list
@input_error
def show_phone(args, book: AddressBook):
    """Shows a contact information

    Args:
        args (list): contains name and phone number
        book (class): contact list

    Returns:
        str: a message with information about the contact,
        or that the contact was not found
    """
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact {name} not found.")
    return record


@empty_contact_list
def show_all(book: AddressBook):
    """Shows all contacts in the list

    Args:
        contacts (dict): contact list

    Returns:
        str: message with a list of contacts
    """
    headers = ["Address Book"]
    return table_show(headers, book.data.items())


@empty_contact_list
@input_error
def delete_contact(args, book: AddressBook):
    """Function to delete one contact or all at once

    Args:
        args (list): contains name and phone number
        book (class): contact list

    Returns:
        str: message about deleting one or all contacts
    """
    name, *_ = args

    record = book.find(name)
    if record:
        book.delete(name)
        return f"The {name} has been deleted"

    if name == "all":  # видалити всі контакти
        book.data.clear()
        return "All contacts have been deleted"

    return f"The {name} is not found"


@empty_contact_list
@input_error
def search_contact(args, book: AddressBook):
    """Search a contact in the book by name, phone or email

    Args:
        * args (list): contains name, phone number or email

    Returns:
        * record: founded contact or warning message
    """
    search_string, *_ = args
    search_string = search_string.strip()
    message = f"No contact with data '{search_string}' was found"
    record_by_name = book.find(search_string)
    if record_by_name:
        return record_by_name
    record_by_phone = book.find_by_phone(search_string)
    if record_by_phone:
        return record_by_phone
    record_by_email = book.find_email(search_string)
    if record_by_email:
        return record_by_email
    return message


@input_error
def add_email_to_contact(args, book: AddressBook):
    """Function to add email to contact

    Args:
        args (list): contains name and email
        book (class): contact list

    Returns:
        str: message email added
    """
    name, email, *_ = args
    record = book.find(name)
    if record:
        record.add_email(email)
        return "Email added"
    else:
        return f"There is no contact {name}"


@empty_contact_list
@input_error
def add_phone_to_contact(args, book: AddressBook):
    """Function to add phone to contact

    Args:
        args (list): contains name and phone number
        book (class): contact list

    Returns:
        str: message phone added
    """
    name, number, *_ = args
    record = book.find(name)
    if record:
        record.add_phone(number)
        return "Phone added"
    else:
        return f"There is no contact {name}"


@empty_contact_list
@input_error
def add_address_to_contact(args, book: AddressBook):
    """Function to add address to contact

    Args:
        args (list): contains name and address
        book (class): contact list

    Returns:
        str: message address added
    """
    name, *address = args
    if len(address) == 1:
        address_for_record = address[0]
    else:
        address_for_record = ""
        for world in address:
            address_for_record += f"{world} "
    record = book.find(name)
    if record:
        record.add_address(address_for_record)
        return "Address added"
    else:
        return f"There is no contact {name}"

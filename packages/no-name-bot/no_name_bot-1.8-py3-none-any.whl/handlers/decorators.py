"""Decorators that handle input errors are collected here."""


def input_error(func):
    """Handles a missing arguments error

    Args:
        func (callable): function
    """

    def inner(*args, **kwargs):
        # parse_input_message = ("Invalid command")
        add_contact_message = (
            "Arguments are required. Print 'add name 1234567890', "
            "where name is contact's name, and 1234567890 is contacts phone number: "
            "10 digits numbers only."
        )
        change_contact_message = "Arguments are required. Print 'change name \
number new-number', where name is contact's name, and number is old \
number and then a new number: 10 digits numbers only."
        show_phone_message = "Argument is required. Print 'phone name', \
where name is contact's name."
        delete_contact_message = (
            "Argument is required. Print 'delete all', or 'delete name'."
        )
        add_birthday_message = "DD.MM.YYYY is format for birthday date."
        show_birthday_message = "Arguments are required. Print 'show-birthday name', \
where name is contact's name."
        show_add_phone_message = (
            "The phone number must contain 10 digits, only numbers are required"
        )
        show_edit_contact_input_message = (
            "Arguments are required. Enter edit-contact <name>"
        )
        search_contact_message = (
            "Arguments are required. Enter search-contact <name> | <email> | <phone>"
        )
        common_message = "Arguments are required."

        try:
            return func(*args, **kwargs)
        except IndexError as i:
            if func.__name__ == "show_phone":
                return show_phone_message
            if func.__name__ == "delete_contact":
                return delete_contact_message
            if func.__name__ == "show_birthday":
                return show_birthday_message
            if func.__name__ == "show_upcoming_birthdays":
                return str(i).strip("'")
            return common_message
        except ValueError:
            if func.__name__ == "add_contact":
                return add_contact_message
            if func.__name__ == "change_contact":
                return change_contact_message
            if func.__name__ == "show_phone":
                return show_phone_message
            if func.__name__ == "delete_contact":
                return delete_contact_message
            if func.__name__ == "add_birthday":
                return add_birthday_message
            if func.__name__ == "show_birthday":
                return show_birthday_message
            if func.__name__ == "add_phone_to_contact":
                return show_add_phone_message
            if func.__name__ == "edit_contact_input":
                print(show_edit_contact_input_message)
            if func.__name__ == "search_contact":
                return search_contact_message
            return common_message
        except KeyError as e:
            if func.__name__ == "edit_contact_input":
                print(str(e).strip('"'))

            return str(e).strip("'")

    return inner


def empty_contact_list(func):
    """handles an empty contact list error

    Args:
        func (callable): any function that depends on the fullness of the contact list
    """

    def inner(*args, **kwargs):
        if len(args) <= 1:
            if len(args[0]) == 0:
                return "The contacts list is empty. \
Type 'add-contact' to add your first contact."
        elif len(args) > 1:
            if len(args[1]) == 0:
                return "The contacts list is empty. \
Type 'add-contact' to add your first contact."
        return func(*args, **kwargs)

    return inner

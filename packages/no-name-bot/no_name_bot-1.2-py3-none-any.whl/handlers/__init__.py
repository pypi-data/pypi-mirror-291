"""This module provides handler functions for parsing input, managing contacts,
and handling birthdays."""

from handlers.birthday_handlers import (
    add_birthday_to_contact,
    show_birthday,
    show_upcoming_birthdays,
)

from handlers.contacts_handlers import (
    add_contact,
    change_contact,
    delete_contact,
    show_all,
    show_phone,
    search_contact,
    add_email_to_contact,
    add_phone_to_contact,
    add_address_to_contact,
)

from handlers.notes_handlers import (
    add_note,
    show_all_notes,
    edit_note,
    remove_note,
    find_note,
    add_tag,
    add_tags,
    remove_tag,
    remove_tags,
    edit_tag,
    all_tags,
    note_tags,
    sort_by_tag
)

from handlers.parse_input import parse_input
from handlers.input_handlers.add_contact_input import (
    add_contact_input
)

from handlers.input_handlers.edit_contact_input import (
    edit_contact_input
)


from handlers.input_handlers.tag_input import (
    add_tag_input, 
    add_tags_input,
    remove_tag_input,
    remove_tags_input,
    edit_tag_input,
    search_note_tags,
    sort_by_tag_input
)

from handlers.validations import (
    input_name_validation,
    input_number_validation,
    input_email_validation,
    input_address_validation,
    input_birthday_validation,
    input_tag_validation,
)

__all__ = [
    "parse_input",
    "add_contact",
    "change_contact",
    "show_all",
    "show_phone",
    "delete_contact",
    "add_birthday_to_contact",
    "show_birthday",
    "show_upcoming_birthdays",
    "add_note",
    "show_all_notes",
    "search_contact",
    "add_email_to_contact",
    "add_phone_to_contact",
    "add_address_to_contact",
    "add_contact_input",
    "input_name_validation",
    "input_number_validation",
    "input_email_validation",
    "input_address_validation",
    "input_birthday_validation",
    "edit_note",
    "remove_note",
    "find_note",
    "edit_contact_input",
    "add_tag",
    "add_tags",
    "remove_tag",
    "remove_tags",
    "edit_tag",
    "all_tags",
    "note_tags",
    "input_tag_validation",
    "add_tag_input",
    "add_tags_input",
    "remove_tag_input",
    "remove_tags_input",
    "edit_tag_input",
    "search_note_tags",
    "sort_by_tag",
    "sort_by_tag_input"
]

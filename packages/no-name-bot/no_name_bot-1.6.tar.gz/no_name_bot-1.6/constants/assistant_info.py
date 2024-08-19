ADDRESSBOOK_COMMANDS = [
    {"command": "hello", "usage": "hello", "exmp": "hello", "desc": "Greets the user."},
    {
        "command": "info",
        "usage": "info",
        "exmp": "info",
        "desc": (
            "Provides general information about the address book "
            "and the notebook commands."
        ),
    },
    {
        "command": "info-addressbook",
        "usage": "info-addressbook",
        "exmp": "info-addressbook",
        "desc": "Displays information about the address book.",
    },
    {
        "command": "add-contact",
        "usage": "add-contact",
        "exmp": "add-contact",
        "desc": "Adds a new contact to the address book.",
    },
    {
        "command": "edit-contact",
        "usage": "edit-contact <name>",
        "exmp": "edit-contact bob",
        "desc": "Edits contact.",
    },
    {
        "command": "delete-contact",
        "usage": "delete-contact <name> OR delete all",
        "exmp": "delete-contact bob OR delete all",
        "desc": "Deletes a specific contact or all contacts from the address book.",
    },
    {
        "command": "phone",
        "usage": "phone <name>",
        "exmp": "phone bob",
        "desc": "Displays the phone number of the specified contact.",
    },
    {
        "command": "search-contact",
        "usage": "search-contact <name/phone/email>",
        "exmp": "search-contact bob",
        "desc": "Searches for a contact by name, phone number, or email address.",
    },
    {
        "command": "show-birthday",
        "usage": "show-birthday <name>",
        "exmp": "show-birthday bob",
        "desc": "Displays the birthday of the specified contact.",
    },
    {
        "command": "birthdays",
        "usage": "birthdays",
        "exmp": "birthdays",
        "desc": "Lists all upcoming birthdays in the range of given days.",
    },
    {
        "command": "all-contacts",
        "usage": "all-contacts",
        "exmp": "all-contacts",
        "desc": "Displays all contacts in the address book.",
    },
    {
        "command": "close",
        "usage": "close",
        "exmp": "close",
        "desc": "Saving Addressbook data and closes the application.",
    },
    {
        "command": "exit",
        "usage": "exit",
        "exmp": "exit",
        "desc": "Exits the address book application.",
    }
]

ADDRESSBOOK_INFO_TABLE_HEADERS = ["COMMAND", "USAGE", "EXAMPLE", "DESCRIPTION"]
ADDRESSBOOK_INFO_TABLE_DATA = [
    [c["command"], c["usage"], c["exmp"], c["desc"]] for c in ADDRESSBOOK_COMMANDS
]

NOTEBOOK_COMMANDS = [
    {"command": "hello", "usage": "hello", "exmp": "hello", "desc": "Greets the user."},
    {
        "command": "info",
        "usage": "info",
        "exmp": "info",
        "desc": (
            "Provides general information about the address book "
            "and the notebook commands."
        ),
    },
    {
        "command": "info-notebook",
        "usage": "info-notebook",
        "exmp": "info-notebook",
        "desc": "Displays information about the notebook.",
    },
    {
        "command": "add-note",
        "usage": "add-note",
        "exmp": "add-note",
        "desc": "Adds a new note with the specified name and text.",
    },
    {
        "command": "edit-note",
        "usage": "edit-note <name>/<text>",
        "exmp": "edit-note name OR text",
        "desc": "Edits note name or text and save it in the Notebook",
    },
    {
        "command": "delete-note",
        "usage": "delete-note <name>/<all>",
        "exmp": "delete-note test OR all",
        "desc": "Removes a specific note by name or all notes if name is 'all'",
    },
    {
        "command": "search-note",
        "usage": "search-note <name>",
        "exmp": "search-note <name>",
        "desc": "Searches for a note by the note name or keyword",
    },
    {
        "command": "all-notes",
        "usage": "all notes",
        "exmp": "all-notes",
        "desc": "Displays all notes in the notebook.",
    },
    {
        "command": "close",
        "usage": "close",
        "exmp": "close",
        "desc": "Saving Addressbook data and closes the application.",
    },
    {
        "command": "exit",
        "usage": "exit",
        "exmp": "exit",
        "desc": "Exits the address book application.",
    },
    {
        "command": "add-tag",
        "usage": "add-tag <note-name> <tag>",
        "exmp": "add-tag todo @task",
        "desc": "Adds a single tag to a note. Use this command to associate a new tag with a note.",
    },
    {
        "command": "add-tags",
        "usage": "add-tags <note-name> <tag>",
        "exmp": "add-tags todo @task @task @task ",
        "desc": "Adds multiple tags to a note. Use this command to associate multiple new tags with a note.",
    },
    {
        "command": "remove-tag",
        "usage": "remove-tag <note_name> <tag>",
        "exmp": "remove-tag todo @task",
        "desc": "Removes a single tag from a note. Use this command to disassociate a tag from a note.",
    },
    {
        "command": "edit-tag",
        "usage": "edit-tag <note-name> <old_tag> <new_tag>",
        "exmp": "edit-tag todo @task @list",
        "desc": "Edits a tag on a note. Use this command to rename a tag associated with a note.",
    },
    {
        "command": "note-tags",
        "usage": "note-tags <note-name> ",
        "exmp": "note-tags todo",
        "desc": "Displays all tags associated with a note. Use this command to view the tags associated with a note.",
    },
    {
        "command": "all-tags",
        "usage": "all-tags",
        "exmp": "all-tags",
        "desc": "Displays all tags in the notebook. Use this command to view all available tags.",
    },
]

NOTEBOOK_INFO_TABLE_HEADERS = ["COMMAND", "USAGE", "EXAMPLE", "DESCRIPTION"]
NOTEBOOK_INFO_TABLE_DATA = [
    [c["command"], c["usage"], c["exmp"], c["desc"]] for c in NOTEBOOK_COMMANDS
]

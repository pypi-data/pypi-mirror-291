"""class NotesBook"""

from collections import UserDict


class NotesBook(UserDict):
    """
    A class to manage a collection of notes.

    Inherits from UserDict to store and manage Note instances.

    Attributes:
        data (dict): A dictionary to store notes using their name as the key.
    """

    def __init__(self):
        """
        Initializes a NotesBook instance.
        """
        super().__init__()

    def __str__(self):
        """
        Returns a string representation of all notes in the NotesBook.

        Returns:
            str: A formatted string with each note's details.
        """
        lines = [str(note) for note in self.data.values()]
        return "\n".join(lines)

    def add_note(self, note):
        """
        Adds a note to the NotesBook.

        Args:
            note (Note): The note to add.

        Raises:
            KeyError: If a note with the same name already exists.
        """
        if note.name.value in self.data:
            raise KeyError(f"Note with name '{note.name.value}' already exists.")
        self.data[note.name.value] = note

    def find(self, name):
        """
        Finds a note by its name.

        Args:
            name (str): The name of the note to find.

        Returns:
            Note or None: The note if found, or None if not found.
        """
        return self.data.get(name, None)

    def delete(self, note_name):
        """
        Deletes a note by name.

        Args:
            * name(str) - The name of the note to be deleted.
        """
        if note_name not in self.data:
            raise KeyError(f"Note with name '{note_name}' not found.")
        del self.data[note_name]

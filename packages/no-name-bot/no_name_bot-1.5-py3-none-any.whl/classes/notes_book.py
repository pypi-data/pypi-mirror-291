"""class NotesBook"""

from collections import UserDict
from classes.note import Note
import re


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

    def find(self, name) -> Note:
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
    
    def add_tag(self, note_name, tag) -> str:
        """
        Adds a tag to a note with the given name.

        Args:
            note_name (str): The name of the note to add the tag to.
            tag (str): The tag to add to the note.

        Returns:
            str: The result of adding the tag, either a success message or an error message
                indicating that the note was not found.

        Notes:
            If the note is found, this method delegates to the note's `add_tag` method.
            If the note is not found, returns an error message indicating that the note was not found.
        """
        note = self.find(note_name)
        if note:
            return note.add_tag(tag)
        else:
            return f"Note with this name: {note_name} not found"
        
    def add_tags(self, note_name, tags: str) -> str:
        """
        Adds tags to a note with the given name.

        Args:
            note_name (str): The name of the note to add tags to.
            tags (str): A string of tags to add, separated by commas.

        Returns:
            str: A success message if the tags are added, or an error message if the note is not found.
        """
        note = self.find(note_name)
        if note:
             tags = self.__split_tags(tags)
             for tag in tags:
                note.add_tag(tag)
             return "Tags added succesfully"
        else:
             return f"Note with this name: {note_name} not found"

    def edit_tag(self, note_name, old_tag, new_tag) -> str:
        """
        Edits a tag in a note with the given name.

        Args:
            note_name (str): The name of the note to edit the tag in.
            old_tag (str): The old tag to replace.
            new_tag (str): The new tag to replace with.

        Returns:
            str: A success message if the tag is edited, or an error message if the note is not found.
        """
        note = self.find(note_name)
        if note:
            return note.edit_tag(old_tag, new_tag)
        else:
            return f"Note with this name: {note_name} not found"        

        
    def remove_tag(self, note_name, tag) -> str:
        """
        Removes a tag from a note with the given name.

        Args:
            note_name (str): The name of the note to remove the tag from.
            tag (str): The tag to remove.

        Returns:
            str: A success message if the tag is removed, or an error message if the note is not found.
        """
        note = self.find(note_name)
        if note:
            return note.remove_tag(tag)
        else:
            return f"Note with this name: {note_name} not found"
        
    def remove_tags(self, note_name, tags: str) -> str:
        """
        Removes multiple tags from a note with the given name.

        Args:
            note_name (str): The name of the note to remove the tags from.
            tags (str): A string of tags to remove, separated by commas.

        Returns:
            str: A success message if the tags are removed, or an error message if the note is not found.
        """
        note = self.find(note_name)
        if note:
             tags = self.__split_tags(tags)
             for tag in tags:
                    note.remove_tag(tag)
             return "Tags removed succesfully"
        else:
             return f"Note with this name: {note_name} not found"     
    
    def find_tag(self, note_name, tag) -> str:
        """
        Finds a tag in a note with the given name.

        Args:
            note_name (str): The name of the note to find the tag in.
            tag (str): The tag to find.

        Returns:
            str: A success message if the tag is found, or an error message if the note is not found.
        """
        note = self.find(note_name)
        if note:
            return note.find_tag(tag)
        else:
            return f"Note with this name: {note_name} not found"
        
    def find_note_tags(self, note_name) -> str:
        """
        Finds all tags in a note with the given name.

        Args:
            note_name (str): The name of the note to find the tags in.

        Returns:
            str: A string of all tags in the note, or an error message if the note is not found.
        """
        note = self.find(note_name)
        if note:
            return note.tags
        else:
            return f"Note with this name: {note_name} not found"
        
    def all_tags(self) -> set:
        """
        Finds all unique tags across all notes.

        Returns:
            set: A set of all unique tags.
        """
        tags = set()
        if len(self.data) > 0:
            for note in self.data.values():
                tags.update(note.tags)
        return tags
    
    def sort_by_tag(self, order: str = 'asc'):
        """
        Sorts notes in ascending or descending order by tags.

        Args:
            order (str): The order to sort in ('asc' or 'desc'). Default is 'asc'.

        Returns:
            list: A list of notes in the specified order.
        """
        if order == 'asc':
            return sorted(self.data.values(), key=lambda x: list(x.tags)[0])
        elif order == 'desc':
            return sorted(self.data.values(), key=lambda x: list(x.tags)[0], reverse=True)
        else:
            raise ValueError("Invalid order parameter. Must be 'asc' or 'desc'.")
            
    def __split_tags(self, tags: str) -> list:
        """
        Splits a string of tags into individual tags.' or 'desc'.")

        Args:
            tags (str): A string of tags, separated by something.

        Returns:
            list: A list of individual tags.
        """
        return re.findall(r"#\w+", tags)

"""class Note"""

from classes.field import Field

class Note:
    """
    A class representing a note with a name and text.

    Attributes:
        name (Field): The name of the note.
        text (Field): The text content of the note.
    """

    def __init__(self, name, text=""):
        """
        Initializes a Note instance with a name and optional text.

        Args:
            name (str): The name of the note.
            text (str, optional): The text content of the note. Defaults to empty string.
        """
        self.text = Field(text)
        self.name = Field(name)
        self.__tags = set()

    def __str__(self):
        """
        Returns a string representation of the note.

        Returns:
            str: A formatted string with the note's name and text.
        """
        return f"Note: {self.name.value}, Text: {self.text.value}, Tag: {self.tags}"
    
    def __repr__(self):
        return f"Note: {self.name.value}, Text: {self.text.value}, Tag: {self.tags}"
    
    def __getstate__(self):
        return {'text': self.text, 'name': self.name, 'tags': self.__tags}

    def __setstate__(self, state):
        self.text = state['text']
        self.name = state['name']
        self.__tags = state['tags']

    def edit_name(self, new_name):
        """A function for editing note name"""
        if new_name:
            self.name.value = new_name

    def edit_note(self, new_text):
        """A function for editing note text"""
        if new_text:
            self.text.value = new_text
        return f"Note: {self.name.value}, Text: {self.text.value}, Tag: {self.tags}"
    
    @property
    def tags(self) -> set:
        """A function for getting note tags"""
        return self.__tags
    
    def add_tag(self, tag: str) -> str:
        """A function for adding a tag to the note"""
        if not self.has_tag(tag):
            self.__tags.add(tag)
            return f"{tag} added successfully"
        else:
            return f"{tag} already is used for note"

        
    def remove_tag(self, tag: str):
        """A function for removing a tag from the note"""
        if self.has_tag(tag):
            self.__tags.remove(tag)
            return f"{tag} removed successfully"
        else:
            return f"{tag} not use for this note"
        
    def edit_tag(self, old_tag: str, new_tag: str):
        """A function for editing a tag in the note"""
        if self.has_tag(old_tag):
            self.__tags.remove(old_tag)
            self.__tags.add(new_tag)
            return f"{old_tag} changed successfully"
        else:
            return f"{old_tag} not use for this note"
        
    def find_tag(self, tag: str) -> str:
        """A function for finding a tag in the note"""
        if self.has_tag(tag):
            return self.__str__()
        
    def has_tag(self, tag: str) -> bool:
        """A function for checking if a tag is in the note"""
        return tag in self.__tags      

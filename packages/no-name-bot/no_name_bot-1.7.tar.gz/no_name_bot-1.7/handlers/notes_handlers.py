from classes import NotesBook, Note
from helpers.assistant_info import table_show

headers = ["Note Name", "Text", "Tags"]
header = ["Tags"]

def handle_errors(func):
    """
    Decorator to handle errors and provide user-friendly messages.

    Args:
        func (function): The function to wrap with error handling.

    Returns:
        function: The wrapped function with error handling.
    """

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            return f"Error: {str(e)}"
        except ValueError as e:
            return f"Invalid input: {str(e)}"
        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

    return wrapper


@handle_errors
def add_note(notebook: NotesBook):
    """
    Adds a new note to the notes list.

    Args:
        notebook (NotesBook): The notes list.

    Returns:
        str: Message indicating that the note has been added or an error occurred.
    """
    name = input("Enter note name: ").strip()
    if name:
        text = input("Enter note text: ")
        if text:
            note = notebook.find(name)
            if note is None:
                note = Note(name, text)
                notebook.add_note(note)
                return "Note added."
            else:
                return f"Note with name '{name}' already exists."
        else:
            return "Text cannot be empty."
    else:
        return "Name cannot be empty."


@handle_errors
def show_all_notes(notebook: NotesBook):
    """
    Shows all notes in the list.

    Args:
        notebook (NotesBook): The notes list.

    Returns:
        str: Formatted string with all notes or an error message.
    """
    if not notebook.data:
        return "No notes found."

    rows = [(note.name.value, note.text.value, ' '.join(note.tags)) for note in notebook.data.values()]
    return table_show(headers, rows)


@handle_errors
def find_note(notebook: NotesBook):
    """Finds and returns notes by searching for a keyword in their
    names from the notebook.
    Handles user input directly.
    Args:
        notebook (NotesBook): The notebook to search in.
    Returns:
        str: The notes that match the search, or a message if no matches are found."""

    while True:
        note_name = input("Enter the note name or keyword: ").strip().lower()
        if note_name:
            matching_notes = [
                note
                for note in notebook.data.values()
                if note_name in str(note.name).lower()
            ]
            if matching_notes:
                rows = [(str(note.name), str(note.text), " ".join(note.tags)) for note in matching_notes]
                return table_show(headers, rows)
            else:
                return "No notes found matching that keyword."
        if note_name == "no":
            break


@handle_errors
def edit_note(notebook: NotesBook):
    """
    Edits the text of an existing note in the notebook.

    Prompts the user to enter the name of the note they wish to edit.
    If the note is found, it asks for the new text and updates the note.
    If the note is not found, or if the new text is empty, an appropriate
    message is returned.

    Args:
        notebook (NotesBook): The notebook instance containing notes.

    Returns:
        str: The updated note if the operation is successful, or an error message
            if the note is not found or if the new text is empty.
    """
    name = input("Enter note name: ").strip()
    note = notebook.find(name)
    if note:
        while True:
            usr_chose = input("What do you want to change: (name/text): ").strip()
            if usr_chose == "name":
                while True:
                    new_name = input("Type new name or back to go back: ").strip()
                    if new_name == "back":
                        break
                    elif new_name:
                        note.edit_name(new_name)
                        notebook.add_note(note)
                        notebook.delete(name)
                        return "Name changed."
                    else:
                        print("Type the name, should not be empty.")

            elif usr_chose == "text":
                while True:
                    text = input("Type new text or back to go back: ").strip()
                    if text == "back":
                        break
                    elif text:
                        note.edit_note(text)
                        return "Text changed."
                    else:
                        print("Type the name, should not be empty.")

            elif usr_chose == "exit":
                return "Editing completed."

            else:
                print("Command not found. If you don't want to edit note type | exit |")
    else:
        return f"Note {name} haven't found!"


def remove_note(note_name: str, notebook: NotesBook):
    """
    Removes a note from the notebook.
    Prompts the user to enter the name of the note they wish to remove.
    If the note is found, it is removed from the notebook.
    If the note is not found, an appropriate message is returned.

    Args:
        notebook (NotesBook): The notebook instance containing notes.

    Returns:
        str: message
    """
    if note_name:
        note = notebook.find(note_name)
        if note:
            notebook.delete(note_name)
            return f"Note {note_name} has been deleted."

        if note_name == "all":
            notebook.data.clear()
            return "All notes have been deleted."
        else:
            return "Note not found."
    else:
        return "Please enter: remove-note <name> or remove-note <all>."


@handle_errors
def add_tag(note, tag, notebook: NotesBook):
    """
    Adds a tag to a note in the notebook.

    Args:
        note (str): The name of the note to add the tag to.
        tag (str): The tag to add to the note.
        notebook (NotesBook): The notebook to add the tag to.

    Returns:
        None
    """
    return notebook.add_tag(note, tag)

@handle_errors
def add_tags(args, notebook: NotesBook):
    """
    Adds multiple tags to a note in the notebook.

    Args:
        args (tuple): A tuple containing the note name and a list of tags to add.
        notebook (NotesBook): The notebook to add the tags to.

    Returns:
        None
    """
    note_name, tags = args 
    return notebook.add_tags(note_name, tags)

@handle_errors
def edit_tag(note, old_tag, new_tag, notebook: NotesBook):
    """
    Edits a tag on a note in the notebook.

    Args:
        note (str): The name of the note to edit the tag on.
        old_tag (str): The old tag to replace.
        new_tag (str): The new tag to replace the old tag with.
        notebook (NotesBook): The notebook to edit the tag in.

    Returns:
        None
    """
    return notebook.edit_tag(note, old_tag, new_tag)

@handle_errors
def remove_tag(note, tag, notebook: NotesBook):
    """
    Removes a tag from a note in the notebook.

    Args:
        note (str): The name of the note to remove the tag from.
        tag (str): The tag to remove from the note.
        notebook (NotesBook): The notebook to remove the tag from.

    Returns:
        None
    """
    return notebook.remove_tag(note, tag)

@handle_errors
def remove_tags(args, notebook: NotesBook):
    """
    Removes multiple tags from a note in the notebook.

    Args:
        args (tuple): A tuple containing the note name and a list of tags to remove.
        notebook (NotesBook): The notebook to remove the tags from.

    Returns:
        None
    """
    note_name, tags = args 
    return notebook.remove_tags(note_name, tags)

@handle_errors
def note_tags(note, notebook: NotesBook):
    """
    Retrieves the tags associated with a note in the notebook.

    Args:
        note (str): The name of the note to retrieve the tags for.
        notebook (NotesBook): The notebook to retrieve the tags from.

    Returns:
        list: A list of tags associated with the note.
    """
    tags = notebook.find_note_tags(note)
    if len(tags) > 0:
        rows = [[tag] for tag in tags]
        return table_show(header, rows)
    else:
        return 'No tags found for this note'

@handle_errors
def all_tags(notebook: NotesBook):
    """
    Retrieves all tags in the notebook.

    Args:
        notebook (NotesBook): The notebook to retrieve the tags from.

    Returns:
        list: A list of all tags in the notebook.
    """
    tags = notebook.all_tags()
    if len(tags) > 0:
        rows = [[tag] for tag in tags]
        return table_show(header, rows)
    else:
        return 'No tags at all' 

@handle_errors
def sort_by_tag(order:str, notebook: NotesBook):
    """
    Sorts the notes in the notebook by tag in the specified order.

    Args:
        order (str): The order in which to sort the notes (e.g. "asc" or "desc")
        notebook (NotesBook): The notebook to sort

    Returns:
        str: A string representation of the sorted notebook
    """
    sorted_notes = notebook.sort_by_tag(order)
    if sorted_notes:
        rows = [(note.name.value, note.text.value, ' '.join(note.tags)) for note in sorted_notes]
        return table_show(headers, rows)
    else:
        return 'No notes found'
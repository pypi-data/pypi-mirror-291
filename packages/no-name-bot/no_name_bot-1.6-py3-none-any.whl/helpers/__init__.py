"""
This module provides helper functions for working with the assistant,
including retrieving information, setting up logging, and handling data
serialization.

It includes the following functions and objects:

- `assistant_info`: Returns information about the assistant, such as name,
version, and description.
- `setup_logging`: Configures logging in the application. Allows flexible
configuration of log levels, output format, and log storage.
- `save_data`: Serializes and saves data to a file using pickle.
- `load_data`: Loads and deserializes data from a file saved with pickle.

These functions are available for import through the `__all__` declaration.
"""

from helpers.assistant_info import table_show
from helpers.logging_config import setup_logging
from helpers.pickle_utils import load_data, save_data
from helpers.notes_pickle_utils import load_notes, save_notes
from helpers.autocomplete_config import bindings
from helpers.startup_shutdown import welcome, good_bye, display_ascii_welcome_art

__all__ = [
    "setup_logging",
    "save_data",
    "load_data",
    "table_show",
    "save_notes",
    "load_notes",
    "bindings",
    "welcome",
    "good_bye",
    "display_ascii_welcome_art",
]

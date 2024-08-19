"""The function parses the string entered by the user into a command and its arguments.
    """

from .decorators import input_error


@input_error
def parse_input(user_input: str):
    """The function parses the string entered by the user
    into a command and its arguments.

    Args:
        user_input (str): accepts the string entered by the user in the console

    Returns:
        cmd (str), *args (list): the name of the command and
        the list of arguments in lower case
    """

    cmd, *args = user_input.lower().split()
    cmd = cmd.strip()

    return cmd, *args

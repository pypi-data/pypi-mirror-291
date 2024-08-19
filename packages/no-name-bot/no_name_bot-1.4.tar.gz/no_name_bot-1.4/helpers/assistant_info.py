"""A common function that shows possible bot commands in table view."""

import shutil
from tabulate import tabulate


def table_show(headers, data, centred=False):
    """Show data in table view."""
    table = tabulate(
        data,
        headers,
        tablefmt="mixed_grid",
        stralign="left",
    )
    if centred:
        terminal_width = shutil.get_terminal_size().columns
        centered_table = ""
        for line in table.splitlines():
            padding = (terminal_width - len(line)) // 2
            centered_table += " " * max(0, padding) + line + "\n"

        return centered_table
    else:
        return table

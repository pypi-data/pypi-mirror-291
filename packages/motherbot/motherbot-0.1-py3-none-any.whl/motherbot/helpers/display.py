"""
Display module.

The display module contains functions that display data to the user.
"""

import re
import textwrap
from tabulate import tabulate
from ..notes.notes_book import NotesBook
from ..notes.note import Note
from ..helpers.colors import blue, green, yellow, warning


def wrap_text(text: str, width: int = 20) -> str:
    """
    Wraps the given text to a specified width using textwrap.wrap.

    Args:
        text (str): The text to wrap.
        width (int, optional): The maximum width of each line. Defaults to 20.

    Returns:
        str: The wrapped text with lines separated by newline characters.
    """
    return "\n".join(textwrap.wrap(str(text), width=width))


def display_table(headers: list, table: list) -> str:
    """
    Displays a table with the given headers and data.

    Args:
        headers (list): A list of column headers.
        table (list): A list of rows, where each row is a list of values.

    Returns:
        str: The formatted table as a string.
    """
    colored_headers = [blue(header) for header in headers]
    return tabulate(table, headers=colored_headers, tablefmt="grid")


def highlight_term(text: str, term: str, color_code: str = "\033[43m") -> str:
    """
    Highlights the term in the text by changing the background color.
    Args:
        text (str): The text to search in.
        term (str): The term to highlight.
        color_code (str, optional): The ANSI background color code to use for
        highlighting (default is yellow).
    Returns:
        str: The text with the term highlighted with a background color.
    """
    term = re.escape(term)
    highlighted_text = re.sub(
        f'({term})',
        f'{color_code}\\1\033[0m',
        text,
        flags=re.IGNORECASE
    )
    return highlighted_text


def display_notes(book: NotesBook) -> str:
    if not book.data:
        return "Notes book is empty."

    headers = ["Title", "Text", "Tags", "Created On", "Reminder"]
    colored_headers = [blue(header) for header in headers]
    table = []
    for note in book.data.values():
        tags_str = (", ".join([f"#{tag}" for tag in note.tags])
                    if note.tags else " - ")
        reminder_str = str(note.reminder) if note.reminder else " - "
        table.append([
            str(note.title),
            wrap_text(note.text),
            wrap_text(tags_str),
            str(note.created_on),
            reminder_str
        ])

    table_str = tabulate(table, headers=colored_headers, tablefmt="grid")
    return table_str


def display_note(note: Note) -> str:
    headers = ["Title", "Text", "Tags", "Created On", "Reminder"]
    colored_headers = [green(header) for header in headers]
    tags_str = (", ".join([f"#{tag}" for tag in note.tags])
                if note.tags else " - ")
    reminder_str = str(note.reminder) if note.reminder else " - "
    table = [[
        str(note.title),
        wrap_text(note.text),
        wrap_text(tags_str),
        str(note.created_on),
        reminder_str
    ]]

    table_str = tabulate(table, headers=colored_headers, tablefmt="grid")
    return table_str


def display_reminders(book: NotesBook, days: int) -> str:
    notes_with_reminders = book.upcoming_reminders(days)
    if not notes_with_reminders:
        return warning(f"No reminders in the next {days} days.")
    headers = ["Title", "Text", "Tags", "Created On", "Reminder"]
    colored_headers = [yellow(header) for header in headers]
    table = []
    for note in notes_with_reminders:
        tags_str = (", ".join([f"#{tag}" for tag in note.tags])
                    if note.tags else " - ")
        reminder_str = str(note.reminder) if note.reminder else " - "
        table.append([
            str(note.title),
            wrap_text(note.text),
            wrap_text(tags_str),
            str(note.created_on),
            reminder_str
        ])

    table_str = tabulate(table, headers=colored_headers, tablefmt="grid")
    return table_str

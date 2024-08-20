"""
Display module.

The display module contains functions that display data to the user.
"""

import re
import textwrap
from tabulate import tabulate
from fuzzywuzzy import fuzz
from .colors import yellow, success, warning


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
    colored_headers = [yellow(header) for header in headers]
    return tabulate(table, headers=colored_headers, tablefmt="fancy_grid")


def highlight_term(text: str, term: str, threshold: int = 60) -> str:
    """
    Highlights the terms in the text by changing the background color.
    Full matches are highlighted in green, partial matches in yellow.

    Args:
    text (str): The text to search in.
    term (str): The term to highlight.
    threshold (int): The similarity threshold for partial matches.

    Returns:
    str: The text with the terms highlighted with background colors.
    """
    term = term.lower()
    if term in text.lower():
        return re.sub(
            f'({re.escape(term)})',
            lambda match: success(match.group(0)),
            text,
            flags=re.IGNORECASE
        )

    if fuzz.ratio(text.lower(), term) >= threshold:
        return warning(text)

    words = text.split()
    highlighted_words = []

    for word in words:
        similarity = fuzz.ratio(word.lower(), term)
        if similarity >= threshold:
            highlighted_word = warning(word)
        else:
            highlighted_word = word
        highlighted_words.append(highlighted_word)

    return ' '.join(highlighted_words)

"""
Serialize and deserialize address book data
"""

import pickle
from time import sleep
from typing import Union
from rich.progress import Progress
from ..notes.notes_book import NotesBook
from ..contacts.address_book import AddressBook


def save_data(data: Union["AddressBook", "NotesBook"], filename: str) -> None:
    """
    Saves the provided data to a file.

    Args:
        data: The data to be saved, can be of any serializable type.
        filename (str): The name of the file where the data will be saved.

    Returns:
        None
    """
    with Progress() as progress:
        task = progress.add_task(
            f"[blue]Saving data to {filename}...", total=100
        )
        while not progress.finished:
            progress.update(task, advance=100)
            sleep(0.8)
    with open(filename, "wb") as f:
        pickle.dump(data, f)


def load_data(
    filename: str,
    default_data: Union["AddressBook", "NotesBook"] = None
) -> Union["AddressBook", "NotesBook"]:
    """
    Loads data from a file.

    Args:
        filename (str): The name of the file from which the data will be
        loaded.
        default_data: The default data to return if the file is not found.

    Returns:
        The loaded data or default_data if the file is not found.
    """
    with Progress() as progress:
        task = progress.add_task(
            f"[blue]Loading data from {filename}...", total=100
        )
        while not progress.finished:
            progress.update(task, advance=100)
            sleep(0.8)
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return default_data

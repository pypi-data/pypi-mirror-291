from time import sleep
from rich.progress import Progress
from ..helpers.serialize import save_data, load_data
from ..helpers.colors import yellow, blue, gray, danger, success
from ..constants.values import ADDRESS_BOOK_PATH, NOTES_BOOK_PATH
from ..contacts.address_book import AddressBook
from ..notes.notes_book import NotesBook
from ..settings.app_settings import app_settings


def save_books(
    address_book: AddressBook = None,
    notes_book: NotesBook = None
) -> None:
    """
    Saves the `adsress_book` and `notes_book` to disk.

    Args:
        adsress_book (AddressBook) optional: An instance of the `AddressBook`
        class.
        notes_book (NotesBook) optional: An instance of the `NotesBook` class.

    Returns:
        None
    """
    with Progress() as progress:
        task = progress.add_task(
            "[blue]Saving data, please wait...", total=100
        )
        while not progress.finished:
            progress.update(task, advance=100)
            sleep(0.8)
    if address_book:
        save_data(address_book, ADDRESS_BOOK_PATH)
    if notes_book:
        save_data(notes_book, NOTES_BOOK_PATH)


def load_books() -> tuple[AddressBook, NotesBook]:
    """
    Loads the `adsress_book` and `notes_book` from disk.

    Returns:
        tuple[AddressBook, NotesBook]: A tuple of the `adsress_book` and
        `notes_book` objects.
    """
    with Progress() as progress:
        task = progress.add_task(
            "[blue]Loading data, please wait...", total=100
        )
        while not progress.finished:
            progress.update(task, advance=100)
            sleep(0.8)
    book = load_data(ADDRESS_BOOK_PATH, default_data=AddressBook())
    notes_book = load_data(NOTES_BOOK_PATH, default_data=NotesBook())

    return book, notes_book


def get_help() -> None:
    """
    Returns a help message with list of available commands.
    """
    command_names = app_settings.get_command_names()
    command_descriptions = app_settings.get_command_descriptions()
    print()
    for command, info in command_descriptions.items():
        print(f" - {yellow(command_names[command])}: {info["description"]}")
        if info["subcommands"]:
            for subcommand, description in info["subcommands"].items():
                print(f"   - {blue(command_names[subcommand])}: {description}")
    print()


def settings(book: AddressBook) -> str:
    """
    Sets the language for the application.

    Returns:
        str: The language code.
    """
    questions = app_settings.get_questions()
    is_updated = False
    try:
        while True:
            language = input(
                gray(questions["back"])
                + blue(
                    questions["language"]
                    .format("/".join(app_settings.list_languages()))
                    + questions["skip"])).strip().lower()
            if not language:
                break
            if app_settings.language == language:
                break
            try:
                app_settings.language = language
                book.language = language
                is_updated = True
                break
            except ValueError as e:
                print(gray(questions["back"]) + danger(str(e)))
                continue

        while True:
            date_format = input(
                gray(questions["back"])
                + blue(
                    questions["date_format"]
                    .format(", ".join(app_settings.list_date_formats()))
                    + questions["skip"])).strip().upper()
            if not date_format:
                break
            if app_settings.date_str_format == date_format:
                break
            try:
                app_settings.date_format = date_format
                book.date_str_format = date_format
                is_updated = True
                break
            except ValueError as e:
                print(gray(questions["back"]) + danger(str(e)))
                continue

        return (
            success(app_settings.get_info_messages()["settings_changed"])
            if is_updated else
            danger(app_settings.get_info_messages()["operation_cancelled"])
        )
    except KeyboardInterrupt:
        return danger(
            "\n" +
            app_settings.get_info_messages()["operation_cancelled"]
        )

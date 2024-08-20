"""
Controllers module.

The controllers module contains functions that interact with the user and
modify the notes book.
"""

from .general import save_books
from ..notes.notes_book import NotesBook
from ..notes.note import Note
from ..helpers.colors import green, blue, gray, success, warning, danger
from ..helpers.completer import Prompt
from ..helpers.generate_data import generate_random_note
from ..settings.app_settings import app_settings


def add_note(book: NotesBook) -> str:
    """
    Adds a new note to the `book'.

    Args:
        book (NotesBook): An instance of the `NotesBook` class.

    Returns:
        str: A message indicating whether the note was added or
        if the input is invalid.
    """
    questions = app_settings.get_questions()
    validation_errors = app_settings.get_validation_errors()
    info_messages = app_settings.get_info_messages()
    try:
        while True:
            title = input(gray(questions["back"]) + blue(questions["title"]))
            if title.strip().lower() in book.data:
                print(gray(questions["back"]) + warning(
                    validation_errors["duplicate_title"]
                ).format(title))
                continue
            try:
                new_note = Note(title)
                break
            except ValueError as e:
                print(gray(questions["back"]) + danger(str(e)))
                continue

        edit_text(new_note)
        add_tags(new_note)
        edit_reminder(new_note)
        book.add_note(new_note)
        print(book.display_notes([new_note]))
        save_books(notes_book=book)
        return success(info_messages["note_added"])
    except KeyboardInterrupt:
        return danger("\n" + info_messages["operation_cancelled"])


def change_note(book: NotesBook) -> str:
    """
    Edits an existing note in the `notes book`.

    Args:
        book (NotesBook): An instance of the `NotesBook` class.

    Returns:
        str: A message indicating whether the note was edited or not.
    """
    command_names = app_settings.get_command_names()
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()
    is_edited = False
    prompt = Prompt()
    styled_message = {
        questions["back"]: "#808080",
        questions["title"]: "ansiblue"
    }
    try:
        while True:
            title = prompt.styled_prompt(styled_message, list(book))
            try:
                note = book.find(title)
                break
            except ValueError as e:
                print(gray(questions["back"]) + danger(str(e)))
                continue

        print(book.display_notes([note]))
        while True:
            commands = {
                command_names["main_menu"]: None,
                command_names["add_tags"]: add_tags,
            }
            if note.add_tags:
                commands[command_names["remove_tag"]] = remove_tag
            if note.text:
                commands[command_names["edit_text"]] = edit_text
                commands[command_names["remove_text"]] = remove_text
            else:
                commands[command_names["add_text"]] = edit_text
            if note.reminder:
                commands[command_names["remove_reminder"]] = remove_reminder
                commands[command_names["edit_reminder"]] = edit_reminder
            else:
                commands[command_names["add_reminder"]] = edit_reminder
            options = "Options: " + ", ".join(list(commands))
            print(gray(questions["back"] + options))

            styled_message = {
                questions["back"]: "#808080",
                questions["command"]: "ansiblue"
            }
            command = prompt.styled_prompt(styled_message, list(commands))

            if command == command_names["main_menu"]:
                break
            if command in commands:
                commands[command](note)
                is_edited = True
                print(book.display_notes([note]))
            else:
                print(
                    gray(questions["back"])
                    + danger(info_messages["unknown_command"])
                )
                continue
        if is_edited:
            save_books(notes_book=book)
        return (
            success(info_messages["note_edited"])
            if is_edited
            else danger(info_messages["operation_cancelled"])
        )
    except KeyboardInterrupt:
        if is_edited:
            save_books(notes_book=book)
        return (
            success("\n" + info_messages["note_edited"])
            if is_edited
            else danger(info_messages["operation_cancelled"])
        )


def edit_text(note: Note) -> None:
    """
    Edits text in the `note`.

    Args:
        note (Note): An instance of the `Note` class.

    Returns:
        None
    """
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()
    while True:
        try:
            text = input(
                gray(questions["back"])
                + blue(questions["text"] + questions["skip"])
            )
            if not text:
                break
            note.add_text(text)
            print(
                gray(questions["back"])
                + green(info_messages["text_added"])
            )
            break
        except ValueError as e:
            print(gray(questions["back"]) + danger(str(e)))
            continue


def remove_text(note: Note) -> None:
    """
    Removes text from the `note`.

    Args:
        note (Note): An instance of the `Note` class.

    Returns:
        None
    """
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()
    note.remove_text()
    print(gray(questions["back"]) + green(info_messages["text_removed"]))


def add_tags(note: Note) -> None:
    """
    Adds tag to the `note`.

    Args:
        note (Note): An instance of the `Note` class.

    Returns:
        None
    """
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()
    while True:
        try:
            tags = input(
                gray(questions["back"])
                + blue(questions["tags"] + questions["skip"])
            )
            if not tags.strip():
                break
            note.add_tags(tags)
            print(gray(questions["back"]) + green(info_messages["tags_added"]))
            break
        except ValueError as e:
            print(gray(questions["back"]) + danger(str(e)))
            continue


def remove_tag(note: Note) -> None:
    """
    Delete the tag of the `note`.

    Args:
        note (Note): An instance of the `Note` class.
        tag (str): An instance of the `str` class.

    Returns:
        None
    """
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()
    prompt = Prompt()
    styled_message = {
        questions["back"]: "#808080",
        questions["tag"] + questions["skip"]: "ansiblue"
    }
    while True:
        try:
            tag = prompt.styled_prompt(
                styled_message,
                [tag.value for tag in note.tags]
            )
            if not tag:
                break
            note.remove_tag(tag)
            print(
                gray(questions["back"])
                + green(info_messages["tag_removed"])
            )
        except ValueError as e:
            print(gray(questions["back"]) + danger(str(e)))
            continue


def edit_reminder(note: Note) -> None:
    """
    Edits reminder in the `note`.

    Args:
        note (Note): An instance of the `Note` class.

    Returns:
        None
    """
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()
    while True:
        try:
            reminder = input(
                gray(questions["back"])
                + blue(questions["reminder"] + questions["skip"])
            )
            if not reminder:
                break
            note.set_reminder(reminder)
            print(
                gray(questions["back"])
                + green(info_messages["reminder_added"])
            )
            break
        except ValueError as e:
            print(gray(questions["back"]) + danger(str(e)))
            continue


def remove_reminder(note: Note) -> None:
    """
    Removes reminder from the `note`.

    Args:
        note (Note): An instance of the `Note` class.

    Returns:
        None
    """
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()
    note.remove_reminder()
    print(gray(questions["back"]) + green(info_messages["reminder_removed"]))


def get_notes(book: NotesBook) -> str:
    """
    Returns a string containing the title, text, tags, created_on, reminder of
    all notes in the `book`.

    Args:
        book (NotesBook): An instance of the `NotesBook` class.

    Returns:
        str: A string containing title, text, tags, created_on, reminder of
        all notes in the `book`.
    """
    info_messages = app_settings.get_info_messages()
    if not book.data:
        return warning(info_messages["no_notes"])

    return book.display_notes(book.data.values())


def delete_note(book: NotesBook) -> str:
    """
    Deletes a note from the notes book.

    Args:
        book (NotesBook): An instance of the NotesBook class from which
        the note will be deleted.

    Returns:
        str: A success message indicating the deletion of the contact.
    """
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()
    prompt = Prompt()
    styled_message = {
        questions["back"]: "#808080",
        questions["title"]: "ansiblue"
    }
    while True:
        try:
            title = prompt.styled_prompt(styled_message, list(book))
            book.delete(title)
            break
        except ValueError as error:
            print(gray(questions["back"]) + danger(str(error)))
        except KeyboardInterrupt:
            return danger(info_messages["operation_cancelled"])

    save_books(notes_book=book)
    return success(info_messages["note_deleted"])


def fake_notes(book: NotesBook) -> str:
    """
    Generates a specified number of fake notes and adds them to the NotesBook.

    Args:
        book (NotesBook): An instance of the NotesBook class to which the
        fake notes will be added.

    Returns:
        str: A success message indicating the number of fake notes added.
    """
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()
    validation_errors = app_settings.get_validation_errors()
    while True:
        try:
            count = input(gray(questions["back"]) + blue(questions["notes"]))
            if not count.isdigit():
                print(
                    gray(questions["back"])
                    + warning(validation_errors["invalid_number"])
                )
                continue
            count = int(count)
            break
        except KeyboardInterrupt:
            return danger(info_messages["operation_cancelled"])

    for _ in range(count):
        note_data = generate_random_note()
        note = Note(note_data["title"])
        if note_data["text"]:
            note.add_text(note_data["text"])
        for tag in note_data["tags"]:
            note.add_tags(tag)
        if note_data["reminder"]:
            note.set_reminder(note_data["reminder"])
        try:
            book.add_note(note)
        except ValueError as e:
            print(gray(questions["back"]) + danger(str(e)))

    save_books(notes_book=book)
    return success(info_messages["fake_notes_generated"])


def reminders(book: NotesBook) -> str:
    """
    Returns a string containing the titles and reminder dates of all notes
    in the `book` that have a reminder within the next specified number of
    days.

    Args:
        book (NotesBook): An instance of the `NotesBook` class.

    Returns:
        str: A string containing the titles and reminder dates of all notes
        in the `book` that have a reminder within the next specified number
        of days.
        If there are no reminders within the specified period, a warning
        message is returned.
    """
    questions = app_settings.get_questions()
    validation_errors = app_settings.get_validation_errors()
    info_messages = app_settings.get_info_messages()
    while True:
        days = input(gray(questions["back"]) + blue(questions["days"]))
        if not days.isdigit():
            print(
                gray(questions["back"])
                + warning(validation_errors["invalid_number"])
            )
            continue
        notes = book.upcoming_reminders(int(days))
        if not notes:
            return warning(info_messages["no_reminders"].format(days))

        return book.display_notes(notes)


def search_notes(book: NotesBook) -> str:
    """
    Searches for notes in the `NotesBook` that match the given search term.
    The search term can be a note title or a tag.

    Args:
        book (NotesBook): An instance of the `NotesBook` class.

    Returns:
        str: A string containing the notes that match the search term or an
        error message if no results were found.
    """
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()
    while True:
        try:
            search_term = input(
                gray(questions["back"])
                + blue(questions["search_notes"])
            ).strip()
            if not search_term:
                continue

            results = book.smart_search(search_term)
            if results:
                return book.display_notes(results, search_term)

            print(warning(info_messages["no_notes"]))
        except KeyboardInterrupt:
            return danger("\n" + info_messages["operation_cancelled"])

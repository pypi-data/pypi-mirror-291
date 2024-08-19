"""
Controllers module.

The controllers module contains functions that interact with the user and
modify the notes book.
"""

from ..notes.notes_book import NotesBook
from ..notes.note import Note
from ..helpers.colors import green, blue, dim, success, warning, danger
from ..helpers.completer import Prompt
from ..helpers.generate_data import generate_random_note
from ..helpers.display import display_notes, display_note, display_reminders
from ..constants.questions import questions
from ..constants.info_messages import info_messages
from ..constants.commands import commands
from ..constants.validation import validation_errors


def add_note(book: NotesBook) -> str:
    """
    Adds a new note to the `book'.

    Args:
        book (NotesBook): An instance of the `NotesBook` class.

    Returns:
        str: A message indicating whether the note was added or
        if the input is invalid.
    """
    try:
        while True:
            title = input(dim(questions["back"]) + blue(questions["title"]))
            if title.strip().lower() in book.data:
                print(dim(questions["back"]) + warning(
                    validation_errors["duplicate_title"]
                ).format(title))
                continue
            try:
                new_note = Note(title)
                break
            except ValueError as e:
                print(dim(questions["back"]) + danger(str(e)))
                continue

        edit_text(new_note)
        add_tags(new_note)
        edit_reminder(new_note)
        book.add_note(new_note)
        print(display_note(new_note))
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
    is_edited = False
    prompt = Prompt()
    try:
        while True:
            question = dim(questions["back"]) + blue(questions["title"])
            print(question, end="")
            title = prompt.prompt(
                " " * len(questions["back"] + questions["title"]), list(book)
            )
            print("\033[F\033[K", end="")
            print(f"{question}{title}")
            try:
                note = book.find(title)
                break
            except ValueError as e:
                print(dim(questions["back"]) + danger(str(e)))
                continue

        print(display_note(note))
        while True:
            all_commands = {
                commands["main_menu"]: None,
                commands["add_tags"]: add_tags,
            }
            if note.add_tags:
                all_commands[commands["remove_tag"]] = remove_tag
            if note.text:
                all_commands[commands["edit_text"]] = edit_text
                all_commands["remove_text"] = remove_text
            else:
                all_commands["add_text"] = edit_text
            if note.reminder:
                all_commands[commands["remove_reminder"]] = remove_reminder
                all_commands[commands["edit_reminder"]] = edit_reminder
            else:
                all_commands[commands["add_reminder"]] = edit_reminder
            options = f"Options: {", ".join(list(all_commands))}"
            print(dim(questions["back"] + options))
            question = dim(questions["back"]) + blue(questions["command"])
            print(question, end="")
            n = len(questions["back"] + questions["command"])
            command = prompt.prompt(" " * n, list(all_commands))
            print("\033[F\033[K", end="")
            print(f"{question}{command}")

            if command == commands["main_menu"]:
                break
            if command in all_commands:
                all_commands[command](note)
                is_edited = True
                print(display_note(note))
            else:
                print(
                    dim(questions["back"])
                    + danger(info_messages["unknown_command"])
                )
                continue
        return (
            success("\n" + info_messages["note_edited"])
            if is_edited
            else danger(info_messages["operation_cancelled"])
        )
    except KeyboardInterrupt:
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
    while True:
        try:
            text = input(
                dim(questions["back"])
                + blue(questions["text"] + questions["skip"])
            )
            if not text:
                break
            note.add_text(text)
            print(
                dim(questions["back"])
                + green(info_messages["text_added"])
            )
            break
        except ValueError as e:
            print(dim(questions["back"]) + danger(str(e)))
            continue


def remove_text(note: Note) -> None:
    """
    Removes text from the `note`.

    Args:
        note (Note): An instance of the `Note` class.

    Returns:
        None
    """
    note.remove_text()
    print(dim(questions["back"]) + green(info_messages["text_removed"]))


def add_tags(note: Note) -> None:
    """
    Adds tag to the `note`.

    Args:
        note (Note): An instance of the `Note` class.

    Returns:
        None
    """
    while True:
        try:
            tags = input(
                dim(questions["back"])
                + blue(questions["tags"] + questions["skip"])
            )
            if not tags.strip():
                break
            note.add_tags(tags)
            print(dim(questions["back"]) + green(info_messages["tags_added"]))
            break
        except ValueError as e:
            print(dim(questions["back"]) + danger(str(e)))
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
    prompt = Prompt()
    while True:
        try:
            question = dim(questions["back"]) + blue(
                questions["tag"] + questions["skip"]
            )

            print(question, end="")
            n = len(questions["back"] + questions["tag"] + questions["skip"])
            tag = prompt.prompt(" " * n, [tag.value for tag in note.tags])
            print("\033[F\033[K", end="")
            print(f"{question}{tag}")
            if not tag:
                break
            note.remove_tag(tag)
            print(
                dim(questions["back"])
                + green(info_messages["tag_removed"])
            )
        except ValueError as e:
            print(dim(questions["back"]) + danger(str(e)))
            continue


def edit_reminder(note: Note) -> None:
    """
    Edits reminder in the `note`.

    Args:
        note (Note): An instance of the `Note` class.

    Returns:
        None
    """
    while True:
        try:
            reminder = input(
                dim(questions["back"])
                + blue(questions["reminder"] + questions["skip"])
            )
            if not reminder:
                break
            note.set_reminder(reminder)
            print(
                dim(questions["back"])
                + green(info_messages["reminder_added"])
            )
            break
        except ValueError as e:
            print(dim(questions["back"]) + danger(str(e)))
            continue


def remove_reminder(note: Note) -> None:
    """
    Removes reminder from the `note`.

    Args:
        note (Note): An instance of the `Note` class.

    Returns:
        None
    """
    note.remove_reminder()
    print(dim(questions["back"]) + green(info_messages["reminder_removed"]))


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
    if not book.data:
        return warning(info_messages["no_notes"])

    return display_notes(book)


def delete_note(book: NotesBook) -> str:
    """
    Deletes a note from the notes book.

    Args:
        book (NotesBook): An instance of the NotesBook class from which
        the note will be deleted.

    Returns:
        str: A success message indicating the deletion of the contact.
    """
    prompt = Prompt()
    while True:
        try:
            question = dim(questions["back"]) + blue(questions["title"])
            print(question, end="")
            title = prompt.prompt(
                " " * len(questions["back"] + questions["title"]), list(book)
            )
            print("\033[F\033[K", end="")
            print(f"{question}{title}")
            book.delete(title)
            break
        except ValueError as error:
            print(dim(questions["back"]) + danger(str(error)))
        except KeyboardInterrupt:
            return danger(info_messages["operation_cancelled"])
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
    while True:
        try:
            count = input(dim(questions["back"]) + blue(questions["notes"]))
            if not count.isdigit():
                print(
                    dim(questions["back"])
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
            print(dim(questions["back"]) + danger(str(e)))

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
    while True:
        days = input(dim(questions["back"]) + blue(questions["days"]))
        if not days.isdigit():
            print(
                dim(questions["back"])
                + warning(validation_errors["invalid_number"])
            )
            continue
        notes = book.upcoming_reminders(int(days))
        if not notes:
            return warning(info_messages["no_reminders"])

        return display_reminders(book, int(days))


def search_notes(book: NotesBook) -> str:
    """
    Searches for notes in the `NotesBook` that match the given search term.
    The search term can be a note title or a tag. If searching by tag,
    results are sorted by the presence of the tag.

    Args:
        book (NotesBook): An instance of the `NotesBook` class.

    Returns:
        str: A string containing the notes that match the search term.
    """
    while True:
        search_term = input(
            "Enter search term (title or tag) or 'q' to quit: ").strip()
        if search_term.lower() == "q":
            return "Operation canceled."

        if not search_term:
            print("Please enter a valid search term or 'q' to exit.")
            continue

        results_by_title = book.search_notes_by_title(search_term)
        if results_by_title:
            sorted_results_by_title = book.sort_notes_by_title(
                results_by_title)
            return "\n".join([str(note) for note in sorted_results_by_title])

        results_by_tag = book.search_notes_by_tag(search_term)
        if results_by_tag:
            sorted_results_by_tag = book.sort_notes_by_tag(search_term)
            return "\n".join([str(note) for note in sorted_results_by_tag])

        print("No notes found matching the search term.")

"""
Main module.
"""
from .helpers.suggest import suggest_command
from .helpers.completer import Prompt
from .helpers.colors import green, danger, red
from .helpers.welcome import print_title
from .settings.app_settings import app_settings
from .controllers.general import save_books, load_books, get_help, settings
from .controllers.notes_controllers import (
    add_note,
    change_note,
    delete_note,
    get_notes,
    reminders,
    fake_notes,
    search_notes
)
from .controllers.contacts_controllers import (
    add_contact,
    change_contact,
    get_contacts,
    birthdays,
    delete_contact,
    fake_contacts,
    search_contacts,
)


def main():
    """
    The main function that serves as the entry point for the application.
    """
    book, notes_book = load_books()
    app_settings.language = book.language
    app_settings.date_format = book.date_str_format
    print_title("Welcome to the assistant bot!", red)
    print(green(book.upcoming_birthdays(days=7, short=True)))
    print(green(notes_book.upcoming_reminders(days=7, short=True)))
    prompt = Prompt()

    while True:
        command_names = app_settings.get_command_names()
        questions = app_settings.get_questions()

        contacts_controllers = {
            command_names["settings"]: settings,
            command_names["add_contact"]: add_contact,
            command_names["change_contact"]: change_contact,
            command_names["delete_contact"]: delete_contact,
            command_names["all_contacts"]: get_contacts,
            command_names["birthdays"]: birthdays,
            command_names["search_contacts"]: search_contacts,
            command_names["fake_contacts"]: fake_contacts,
        }

        notes_controllers = {
            command_names["add_note"]: add_note,
            command_names["change_note"]: change_note,
            command_names["delete_note"]: delete_note,
            command_names["all_notes"]: get_notes,
            command_names["reminders"]: reminders,
            command_names["search_notes"]: search_notes,
            command_names["fake_notes"]: fake_notes,
        }
        exit_commands = [command_names["close"], command_names["exit"]]

        all_commands = (
            [command_names["help"]] + list(contacts_controllers)
            + list(notes_controllers) + exit_commands
        )
        try:
            styled_message = {questions["command"]: "#FFFFFF"}
            command = prompt.styled_prompt(
                styled_message, all_commands).strip().lower()
        except KeyboardInterrupt:
            save_books(book, notes_book)
            print(green(app_settings.get_info_messages()["goodbye"]))
            break

        if not command:
            continue

        if command not in all_commands:
            similar_command = suggest_command(command, all_commands)
            if similar_command:
                answer = input(questions["suggest"].format(similar_command))
                if answer.lower() in ["y", "yes", "т", "так"]:
                    command = similar_command
                else:
                    continue
            else:
                print(danger(
                    app_settings.get_info_messages()["unknown_command"]
                ))
                continue

        if command in exit_commands:
            save_books(book, notes_book)
            print(green(app_settings.get_info_messages()["goodbye"]))
            break

        if command in contacts_controllers:
            print(contacts_controllers[command](book))

        elif command in notes_controllers:
            print(notes_controllers[command](notes_book))

        elif command == command_names["help"]:
            get_help()


if __name__ == "__main__":
    main()

"""
Main module.
"""
from .helpers.suggest import suggest_command
from .helpers.completer import Prompt
from .helpers.serialize import save_data, load_data
from .helpers.colors import green, danger, red
from .helpers.help import get_help
from .helpers.welcome import print_title
from .notes.notes_book import NotesBook
from .contacts.address_book import AddressBook
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
    interactive_search_with_autocomplete,
)

controllers = {
    "add-contact": add_contact,
    "change-contact": change_contact,
    "delete-contact": delete_contact,
    "all-contacts": get_contacts,
    "birthdays": birthdays,
    "fake-contacts": fake_contacts,
    "help": get_help,
    "search-contacts": search_contacts,
    "smart-search": interactive_search_with_autocomplete,
}
notes_controllers = {
    "add-note": add_note,
    "change-note": change_note,
    "delete-note": delete_note,
    "all-notes": get_notes,
    "fake-notes": fake_notes,
    "reminders": reminders,
    "search-notes": search_notes
}


def main():
    """
    The main function that serves as the entry point for the application.
    """
    book = load_data("address_book.pkl", default_data=AddressBook())
    notes_book = load_data("notes_book.pkl", default_data=NotesBook())
    print_title("Welcome to the motherbot!", red)
    print(green(book.upcoming_birthdays(days=7, short=True)))
    commands = list(controllers) + list(notes_controllers) + ["close", "exit"]
    prompt = Prompt()

    while True:
        try:
            command = prompt.prompt(
                "Enter a command: ", commands).strip().lower()
        except KeyboardInterrupt:
            print("Good bye!")
            save_data(book, "address_book.pkl")
            save_data(notes_book, "notes_book.pkl")
            break

        if not command:
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(notes_book, "notes_book.pkl")
            save_data(book, "address_book.pkl")
            break

        if command == "hello":
            print(green("How can I help you?"))

        elif command in controllers:
            print(controllers[command](book))

        elif command in notes_controllers:
            print(notes_controllers[command](notes_book))

        else:
            similar_commands = suggest_command(command, commands)
            print(danger("Invalid command."))
            if similar_commands and similar_commands != command:
                print("The most similar commands are")
                for cmd in similar_commands:
                    print(f"\t'{cmd}'")


if __name__ == "__main__":
    main()

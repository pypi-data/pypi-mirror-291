from colorama import Fore, Style


def get_help(_) -> str:
    """
    Returns a help message with list of available commands.
    """
    message = f"""
    {Fore.CYAN}Available commands:
    - hello: Displays a welcome message.
    - help: Shows this help message.
    - add-contact: Starts the process of adding a new contact.
                        Will ask for name, phone(s), birthday, email, and address.
    - change-contact: Opens a submenu with commands to change a contact:
        - add-phones: Adds a new phone.
        - remove-phones: Removes phone.
        - add-birthday: Adds a birthday.
        - edit-birthday: Edits the birthday.
        - remove-birthday: Removes the birthday.
        - add-email: Adds an email.
        - edit-email: Edits the email.
        - remove-email: Removes the email.
        - add-address: Adds an address.
        - edit-address: Edits the address.
        - remove-address: Removes the address.
    - delete-contact: Deletes a contact by name.
    - all-contacts: Shows all contacts with their phone numbers.
    - birthdays: Shows upcoming birthdays within the next 7 days.
    - fake-contacts: Generates a specified number of fake contacts and adds them to an address book.
    - search-contacts: Allows you to search for contacts by name or phone number.
    - smart-search: Interactive search with autocomplete suggestions during input.
    - add-note: Starts the process of adding a new note to the notebook.
                        Will ask for text, tag(s), reminder.
    - change-note: Opens a submenu with commands to change the note: 
        - edit-text: Edits the text of the note.
        - add-tags: Adds a tag to the note.
        - remove-tag: Removes the tag from the note.
        - add-reminder:  Adds a reminder to the note.
    - delete-note: Deletes a note from the notebook.
    - all-notes: Shows all notes in the notebook.
    - fake-notes: Generates a specified number of fake notes and adds them to the notebook.
    - reminders: Shows reminders within the next specified number of days.

    - close / exit : Exits the program.{Style.RESET_ALL}
    """
    return message

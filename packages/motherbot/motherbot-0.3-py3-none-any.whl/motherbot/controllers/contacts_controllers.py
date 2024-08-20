"""
Contacts controllers module.

The contacts controllers module contains functions that interact with the user
and modify the address book.
"""

from .general import save_books
from ..contacts.address_book import AddressBook
from ..contacts.record import Record
from ..helpers.colors import green, blue, gray, success, warning, danger
from ..helpers.generate_data import generate_random_contact
from ..helpers.completer import Prompt
from ..settings.app_settings import app_settings


def add_contact(book: AddressBook) -> str:
    """
    Adds a new contact to the `book` if the name is not already in the
    `book` or adds the phone number to an existing contact.

    Args:
        book (AddressBook): An instance of the `AddressBook` class.

    Returns:
        str: A message indicating whether the contact was added or updated, or
        if the input is invalid.
    """
    questions = app_settings.get_questions()
    validation_errors = app_settings.get_validation_errors()
    info_messages = app_settings.get_info_messages()
    try:
        while True:
            name = input(gray(questions["back"]) + blue(questions["name"]))
            if name.strip().lower() in book.data:
                print(
                    gray(questions["back"])
                    + warning(validation_errors["duplicate_name"]).format(name)
                )
                continue
            try:
                new_record = Record(name)
                break
            except ValueError as e:
                print(gray(questions["back"]) + danger(str(e)))
                continue

        add_phones(new_record)
        edit_birthday(new_record)
        edit_email(new_record)
        edit_address(new_record)
        book.add_record(new_record)
        print(book.display_contacts([new_record]))
        save_books(address_book=book)
        return success(info_messages["contact_added"])
    except KeyboardInterrupt:
        return danger("\n" + info_messages["operation_cancelled"])


def change_contact(book: AddressBook) -> str:
    """
    Edits an existing contact in the `book`.

    Args:
        book (AddressBook): An instance of the `AddressBook` class.

    Returns:
        str: A message indicating whether the contact was edited or not.
    """
    command_names = app_settings.get_command_names()
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()

    is_edited = False
    prompt = Prompt()
    styled_message = {
        questions["back"]: "#808080",
        questions["name"]: "ansiblue"
    }
    try:
        while True:
            name = prompt.styled_prompt(styled_message, list(book))

            try:
                contact = book.find(name)
                break
            except ValueError as e:
                print(gray(questions["back"]) + danger(str(e)))
                continue

        print(book.display_contacts([contact]))
        while True:
            commands = {
                command_names["main_menu"]: None,
                command_names["add_phones"]: add_phones,
            }
            if contact.phones:
                commands[command_names["remove_phone"]] = remove_phone
            if contact.birthday:
                commands[command_names["remove_birthday"]] = remove_birthday
                commands[command_names["edit_birthday"]] = edit_birthday
            else:
                commands[command_names["add_birthday"]] = edit_birthday
            if contact.email:
                commands[command_names["remove_email"]] = remove_email
                commands[command_names["edit_email"]] = edit_email
            else:
                commands[command_names["add_email"]] = edit_email
            if contact.address:
                commands[command_names["remove_address"]] = remove_address
                commands[command_names["edit_address"]] = edit_address
            else:
                commands[command_names["add_address"]] = edit_address
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
                commands[command](contact)
                is_edited = True
                print(book.display_contacts([contact]))
            else:
                print(
                    gray(questions["back"])
                    + danger(info_messages["unknown_command"])
                )
                continue
        if is_edited:
            save_books(address_book=book)
        return (
            success(info_messages["contact_edited"])
            if is_edited
            else danger(info_messages["operation_cancelled"])
        )
    except KeyboardInterrupt:
        if is_edited:
            save_books(address_book=book)
        return (
            success(info_messages["contact_edited"])
            if is_edited
            else danger("\n" + info_messages["operation_cancelled"])
        )


def add_phones(contact: Record) -> None:
    """
    Adds a new phone number to the `contact`.

    Args:
        contact (Record): An instance of the `Record` class.

    Returns:
        None
    """
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()
    while True:
        try:
            phone = input(
                gray(questions["back"])
                + blue(questions["phone"] + questions["skip"])
            )
            if not phone.strip():
                break
            contact.add_phone(phone)
            print(
                gray(questions["back"])
                + green(info_messages["phone_added"])
            )
        except ValueError as e:
            print(gray(questions["back"]) + danger(str(e)))
            continue


def remove_phone(contact: Record) -> None:
    """
    Removes a phone number from the `contact`.

    Args:
        contact (Record): An instance of the `Record` class.

    Returns:
        None
    """
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()
    prompt = Prompt()
    styled_message = {
        questions["back"]: "#808080",
        questions["phone"] + questions["skip"]: "ansiblue"
    }
    while True:
        try:
            phone = prompt.styled_prompt(
                styled_message,
                list(map(str, contact.phones))
            )

            if not phone:
                break
            contact.remove_phone(phone)
            print(
                gray(questions["back"])
                + green(info_messages["phone_removed"])
            )
        except ValueError as e:
            print(gray(questions["back"]) + danger(str(e)))
            continue


def edit_birthday(contact: Record) -> None:
    """
    Edits the birthday of the `contact`.

    Args:
        contact (Record): An instance of the `Record` class.

    Returns:
        None
    """
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()
    while True:
        try:
            birthday = input(
                gray(questions["back"])
                + blue(questions["birthday"] + questions["skip"])
            )
            if not birthday:
                break
            contact.add_birthday(birthday)
            print(
                gray(questions["back"])
                + green(info_messages["birthday_added"])
            )
            break
        except ValueError as e:
            print(gray(questions["back"]) + danger(str(e)))
            continue


def remove_birthday(contact: Record) -> None:
    """
    Removes the birthday from the `contact`.

    Args:
        contact (Record): An instance of the `Record` class.

    Returns:
        None
    """
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()
    contact.remove_birthday()
    print(gray(questions["back"]) + green(info_messages["birthday_removed"]))


def edit_address(contact: Record) -> None:
    """
    Edits the address of the `contact`.

    Args:
        contact (Record): An instance of the `Record` class.

    Returns:
        None
    """
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()
    while True:
        try:
            address = input(
                gray(questions["back"])
                + blue(questions["address"] + questions["skip"])
            )
            if not address:
                break
            contact.add_address(address)
            print(
                gray(questions["back"])
                + green(info_messages["address_added"])
            )
            break
        except ValueError as e:
            print(gray(questions["back"]) + danger(str(e)))
            continue


def remove_address(contact: Record) -> None:
    """
    Removes the address from the `contact`.

    Args:
        contact (Record): An instance of the `Record` class.

    Returns:
        None
    """
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()
    contact.remove_address()
    print(gray(questions["back"]) + green(info_messages["address_removed"]))


def edit_email(contact: Record) -> None:
    """
    Edits the email of the `contact`.

    Args:
        contact (Record): An instance of the `Record` class.

    Returns:
        None
    """
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()
    while True:
        try:
            email = input(
                gray(questions["back"])
                + blue(questions["email"] + questions["skip"])
            )
            if not email:
                break
            contact.add_email(email)
            print(
                gray(questions["back"])
                + green(info_messages["email_added"])
            )
            break
        except ValueError as e:
            print(gray(questions["back"]) + danger(str(e)))
            continue


def remove_email(contact: Record) -> None:
    """
    Removes the email from the `contact`.

    Args:
        contact (Record): An instance of the `Record` class.

    Returns:
        None
    """
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()
    contact.remove_email()
    print(gray(questions["back"]) + green(info_messages["email_removed"]))


def delete_contact(book: AddressBook) -> str:
    """
    Deletes a contact from the address book.

    Args:
        book (AddressBook): An instance of the AddressBook class from which
        the contact will be deleted.

    Returns:
        str: A success message indicating the deletion of the contact.
    """
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()
    prompt = Prompt()
    styled_message = {
        questions["back"]: "#808080",
        questions["name"]: "ansiblue"
    }
    while True:
        try:
            name = prompt.styled_prompt(styled_message, list(book))

            book.delete(name)
            break
        except ValueError as error:
            print(gray(questions["back"]) + danger(str(error)))
        except KeyboardInterrupt:
            return danger(info_messages["operation_cancelled"])
    save_books(address_book=book)
    return success(info_messages["contact_deleted"])


def get_contacts(book: AddressBook) -> str:
    """
    Returns a string containing the names and phone numbers of all contacts
    in the `book`.

    Args:
        book (AddressBook): An instance of the `AddressBook` class.

    Returns:
        str: A string containing the names and phone numbers of all contacts
        in the `book`.
    """
    info_messages = app_settings.get_info_messages()
    if not book.data:
        return warning(info_messages["no_contacts"])
    return book.display_contacts(book.data.values())


def birthdays(book: AddressBook) -> str:
    """
    Returns a string containing the names and congratulation dates of all
    contacts in the `book` who have a birthday within the next 7 days.

    Args:
        book (AddressBook): An instance of the `AddressBook` class.

    Returns:
        str: A string containing the names and congratulation dates of all
        contacts in the `book` who have a birthday within the next 7 days.
    """
    questions = app_settings.get_questions()
    validation_errors = app_settings.get_validation_errors()
    while True:
        days = input(gray(questions["back"]) + blue(questions["days"]))
        if not days.isdigit():
            print(
                gray(questions["back"])
                + warning(validation_errors["invalid_number"])
            )
            continue
        return book.upcoming_birthdays(int(days))


def fake_contacts(book: AddressBook) -> str:
    """
    Generates a specified number of fake contacts and adds them to the address
    book.

    Args:
        book (AddressBook): An instance of the AddressBook class to which the
        fake contacts will be added.

    Returns:
        str: A success message indicating the number of fake contacts added.
    """
    questions = app_settings.get_questions()
    validation_errors = app_settings.get_validation_errors()
    info_messages = app_settings.get_info_messages()
    while True:
        try:
            count = input(
                gray(questions["back"])
                + blue(questions["contacts"])
            )
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
        contact = generate_random_contact()
        record = Record(contact["name"])
        for phone in contact["phones"]:
            record.add_phone(phone)
        if contact["birthday"]:
            record.add_birthday(contact["birthday"])
        if contact["email"]:
            record.add_email(contact["email"])
        if contact["address"]:
            record.add_address(contact["address"])
        try:
            book.add_record(record)
        except ValueError as e:
            print(gray(questions["back"]) + danger(str(e)))
    save_books(address_book=book)
    return success(info_messages["fake_contacts_generated"])


def search_contacts(book: AddressBook) -> str:
    """
    Interactive search for contacts in the `book`.

    Args:
        book (AddressBook): An instance of the `AddressBook` class.

    Returns:
        str: A string containing the table of all contacts in the `book` that
        match the search term or an error message if no results were found.
    """
    questions = app_settings.get_questions()
    info_messages = app_settings.get_info_messages()
    while True:
        try:
            search_term = input(
                gray(questions["back"])
                + blue(questions["search_contacts"])
            ).strip()
            if not search_term:
                continue

            results = book.smart_search(search_term)
            if results:
                return book.display_contacts(results, search_term)

            print(warning(info_messages["no_contacts"]))
        except KeyboardInterrupt:
            return danger("\n" + info_messages["operation_cancelled"])

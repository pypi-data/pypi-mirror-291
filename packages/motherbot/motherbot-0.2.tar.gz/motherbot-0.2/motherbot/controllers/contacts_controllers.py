"""
Contacts controllers module.

The contacts controllers module contains functions that interact with the user
and modify the address book.
"""

from ..contacts.address_book import AddressBook
from ..contacts.record import Record
from ..helpers.colors import green, blue, dim, success, warning, danger
from ..helpers.generate_data import generate_random_contact
from ..helpers.completer import Prompt
from ..constants.questions import questions
from ..constants.info_messages import info_messages
from ..constants.commands import commands
from ..constants.validation import validation_errors


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
    try:
        while True:
            name = input(dim(questions["back"]) + blue(questions["name"]))
            if name.strip().lower() in book.data:
                print(
                    dim(questions["back"])
                    + warning(validation_errors["duplicate_name"]).format(name)
                )
                continue
            try:
                new_record = Record(name)
                break
            except ValueError as e:
                print(dim(questions["back"]) + danger(str(e)))
                continue

        add_phones(new_record)
        edit_birthday(new_record)
        edit_email(new_record)
        edit_address(new_record)
        book.add_record(new_record)
        print(book.display_contacts([new_record]))
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
    is_edited = False
    prompt = Prompt()
    try:
        while True:
            question = dim(questions["back"]) + blue(questions["name"])
            print(question, end="")
            name = prompt.prompt(
                " " * len(questions["back"] + questions["name"]), list(book)
            )
            print("\033[F\033[K", end="")
            print(f"{question}{name}")
            try:
                contact = book.find(name)
                break
            except ValueError as e:
                print(dim(questions["back"]) + danger(str(e)))
                continue

        print(book.display_contacts([contact]))
        while True:
            all_commands = {
                commands["main_menu"]: None,
                commands["add_phones"]: add_phones,
            }
            if contact.phones:
                all_commands[commands["remove_phone"]] = remove_phone
            if contact.birthday:
                all_commands[commands["remove_birthday"]] = remove_birthday
                all_commands[commands["edit_birthday"]] = edit_birthday
            else:
                all_commands[commands["add_birthday"]] = edit_birthday
            if contact.email:
                all_commands[commands["remove_email"]] = remove_email
                all_commands[commands["edit_email"]] = edit_email
            else:
                all_commands[commands["add_email"]] = edit_email
            if contact.address:
                all_commands[commands["remove_address"]] = remove_address
                all_commands[commands["edit_address"]] = edit_address
            else:
                all_commands[commands["add_address"]] = edit_address
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
                all_commands[command](contact)
                is_edited = True
                print(book.display_contacts([contact]))
            else:
                print(
                    dim(questions["back"])
                    + danger(info_messages["unknown_command"])
                )
                continue
        return (
            success(info_messages["contact_edited"])
            if is_edited
            else danger(info_messages["operation_cancelled"])
        )
    except KeyboardInterrupt:
        return (
            success(info_messages["contact_edited"])
            if is_edited
            else danger(info_messages["operation_cancelled"])
        )


def add_phones(contact: Record) -> None:
    """
    Adds a new phone number to the `contact`.

    Args:
        contact (Record): An instance of the `Record` class.

    Returns:
        None
    """
    while True:
        try:
            phone = input(
                dim(questions["back"])
                + blue(questions["phone"] + questions["skip"])
            )
            if not phone.strip():
                break
            contact.add_phone(phone)
            print(dim(questions["back"]) + green(info_messages["phone_added"]))
        except ValueError as e:
            print(dim(questions["back"]) + danger(str(e)))
            continue


def remove_phone(contact: Record) -> None:
    """
    Removes a phone number from the `contact`.

    Args:
        contact (Record): An instance of the `Record` class.

    Returns:
        None
    """
    prompt = Prompt()
    while True:
        try:
            question = dim(questions["back"]) + blue(
                questions["phone"] + questions["skip"]
            )

            print(question, end="")
            n = len(questions["back"] + questions["phone"] + questions["skip"])
            phone = prompt.prompt(" " * n, list(map(str, contact.phones)))
            print("\033[F\033[K", end="")
            print(f"{question}{phone}")
            if not phone:
                break
            contact.remove_phone(phone)
            print(
                dim(questions["back"])
                + green(info_messages["phone_removed"])
            )
        except ValueError as e:
            print(dim(questions["back"]) + danger(str(e)))
            continue


def edit_birthday(contact: Record) -> None:
    """
    Edits the birthday of the `contact`.

    Args:
        contact (Record): An instance of the `Record` class.

    Returns:
        None
    """
    while True:
        try:
            birthday = input(
                dim(questions["back"])
                + blue(questions["birthday"] + questions["skip"])
            )
            if not birthday:
                break
            contact.add_birthday(birthday)
            print(
                dim(questions["back"])
                + green(info_messages["birthday_added"])
            )
            break
        except ValueError as e:
            print(dim(questions["back"]) + danger(str(e)))
            continue


def remove_birthday(contact: Record) -> None:
    """
    Removes the birthday from the `contact`.

    Args:
        contact (Record): An instance of the `Record` class.

    Returns:
        None
    """
    contact.remove_birthday()
    print(dim(questions["back"]) + green(info_messages["birthday_removed"]))


def edit_address(contact: Record) -> None:
    """
    Edits the address of the `contact`.

    Args:
        contact (Record): An instance of the `Record` class.

    Returns:
        None
    """
    while True:
        try:
            address = input(
                dim(questions["back"])
                + blue(questions["address"] + questions["skip"])
            )
            if not address:
                break
            contact.add_address(address)
            print(
                dim(questions["back"])
                + green(info_messages["address_added"])
            )
            break
        except ValueError as e:
            print(dim(questions["back"]) + danger(str(e)))
            continue


def remove_address(contact: Record) -> None:
    """
    Removes the address from the `contact`.

    Args:
        contact (Record): An instance of the `Record` class.

    Returns:
        None
    """
    contact.remove_address()
    print(dim(questions["back"]) + green(info_messages["address_removed"]))


def edit_email(contact: Record) -> None:
    """
    Edits the email of the `contact`.

    Args:
        contact (Record): An instance of the `Record` class.

    Returns:
        None
    """
    while True:
        try:
            email = input(
                dim(questions["back"])
                + blue(questions["email"] + questions["skip"])
            )
            if not email:
                break
            contact.add_email(email)
            print(dim(questions["back"]) + green(info_messages["email_added"]))
            break
        except ValueError as e:
            print(dim(questions["back"]) + danger(str(e)))
            continue


def remove_email(contact: Record) -> None:
    """
    Removes the email from the `contact`.

    Args:
        contact (Record): An instance of the `Record` class.

    Returns:
        None
    """
    contact.remove_email()
    print(dim(questions["back"]) + green(info_messages["email_removed"]))


def delete_contact(book: AddressBook) -> str:
    """
    Deletes a contact from the address book.

    Args:
        book (AddressBook): An instance of the AddressBook class from which
        the contact will be deleted.

    Returns:
        str: A success message indicating the deletion of the contact.
    """
    prompt = Prompt()
    while True:
        try:
            question = dim(questions["back"]) + blue(questions["name"])
            print(question, end="")
            name = prompt.prompt(
                " " * len(questions["back"] + questions["name"]), list(book)
            )
            print("\033[F\033[K", end="")
            print(f"{question}{name}")
            book.delete(name)
            break
        except ValueError as error:
            print(dim(questions["back"]) + danger(str(error)))
        except KeyboardInterrupt:
            return danger(info_messages["operation_cancelled"])
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
    if not book.data:
        return warning(info_messages["no_contacts"])
    return book.display_contacts(book.data.values())


# @input_error
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
    while True:
        days = input(dim(questions["back"]) + blue(questions["days"]))
        if not days.isdigit():
            print(
                dim(questions["back"])
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
    while True:
        try:
            count = input(dim(questions["back"]) + blue(questions["contacts"]))
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
            print(dim(questions["back"]) + danger(str(e)))

    return success(info_messages["fake_contacts_generated"])


def search_contacts(book: AddressBook) -> str:
    """
    Searches for contacts in the `book` that match the given search term.

    Args:
        book (AddressBook): An instance of the `AddressBook` class.

    Returns:
        str: A string containing the names and phone numbers of all contacts
        in the `book` that match the given search term.
    """
    while True:
        search_term = input(blue("Enter search term (name or phone number): "))
        if search_term.lower() == "q":
            return danger("Operation canceled.")
        if not search_term:
            print(warning("Please enter a valid search term or q to exit"))
            continue

        results = book.search(search_term)
        if results:
            return book.display_contacts(results, search_term)
        return warning("No contacts found matching the search term.")


def interactive_search_with_autocomplete(book: AddressBook) -> str:
    """
    Interactive search with autocomplete suggestions during input.
    """
    # Get all names from the address book for autocomplete suggestions
    contact_names = [record.name.value for record in book.data.values()]

    prompt = Prompt()

    while True:
        try:
            search_term = prompt.prompt(
                "Enter search term (name or phone number): ", contact_names
            ).strip()
            if search_term.lower() == "q":
                return danger("Operation canceled.")
            if not search_term:
                print(warning("Please enter a valid search term or q to exit"))
                continue

            results = book.smart_search(search_term)
            if results:
                # Here we make sure to pass the search_term to highlight it
                return book.display_contacts(results, search_term)

            print(warning("No contacts found matching the search term."))
        except KeyboardInterrupt:
            return danger("\nOperation canceled.")

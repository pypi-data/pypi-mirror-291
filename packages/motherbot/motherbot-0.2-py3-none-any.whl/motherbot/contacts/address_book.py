"""
Address book module.
"""

from typing import List
from collections import UserDict
from datetime import datetime
from fuzzywuzzy import process
from ..helpers.colors import warning
from ..helpers.display import wrap_text, display_table, highlight_term
from .record import Record
from ..constants.validation import DATE_FORMAT, validation_errors
from ..constants.info_messages import info_messages


class AddressBook(UserDict):
    """
    Address book class which holds records.
    """

    def add_record(self, new_record: Record) -> None:
        """
        Adds a new record to the address book.

        Args:
            new_record (Record): The record to be added.

        Raises:
            ValueError: If a contact with the same name already exists.
        """
        normalized_name = new_record.name.value.lower()
        if normalized_name in self.data:
            raise ValueError(
                validation_errors["duplicate_name"]
                .format(new_record.name.value)
            )
        self.data[normalized_name] = new_record

    def find(self, contact_name: str) -> Record:
        """
        Finds a record in the address book.

        Args:
            contact_name (str): The name of the contact.

        Raises:
            ValueError: If the contact is not found.

        Returns:
            Record: The record with the given name.
        """
        normalized_name = contact_name.strip().lower()
        if normalized_name in self.data:
            return self.data[normalized_name]
        raise ValueError(
            validation_errors["name_not_found"].format(contact_name)
        )

    def delete(self, contact_name: str) -> None:
        """
        Deletes a record from the address book.

        Args:
            contact_name (str): The name of the contact.

        Raises:
            ValueError: If the contact is not found.
        """
        normalized_name = contact_name.lower()
        if normalized_name not in self.data:
            raise ValueError(
                validation_errors["name_not_found"].format(contact_name)
            )
        del self.data[normalized_name]

    def upcoming_birthdays(self, days: int, short: bool = False) -> str:
        """
        Calculate upcoming birthdays within a number of days for a given list
        of users.

        Args:
            days (int): The number of days to check for upcoming birthdays.
            short (bool, optional): If True, the output will be shortened.

        Returns:
            dict: A dictionary with "congratulation_date" keys and
            corresponding "name" values for upcoming birthdays within the
            given number of days.
        """
        today = datetime.today().date()
        upcoming_birthdays = {}

        for contact in self.data.values():
            if contact.birthday is None:
                continue
            birthday = contact.birthday.value
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday.replace(year=today.year + 1)

            if (birthday_this_year - today).days < days:
                upcoming_birthdays[birthday_this_year] = contact.name.value

        sorted_birthdays = [
            [date.strftime(DATE_FORMAT), name]
            for date, name in sorted(upcoming_birthdays.items())
        ]

        if short:
            return (
                info_messages["upcoming_birthdays"]
                .format(len(sorted_birthdays), days)
                if sorted_birthdays else
                info_messages["no_birthdays"].format(days)
            )
        if not sorted_birthdays:
            return warning(info_messages["no_birthdays"].format(days))

        headers = ["Congratulation Date", "Name"]
        return display_table(headers, sorted_birthdays)

    def search(self, search_term: str) -> list:
        """
        Searches for contacts by name or phone number.
        Args:
            search_term (str): The term to search for in the contact names and
            phone numbers.
        Returns:
            list: A list of `Record` instances that match the search term.
        """
        search_term = search_term.lower()
        results = []

        for record in self.data.values():
            if search_term in record.name.value.lower():
                results.append(record)
                continue

            for phone in record.phones:
                if search_term in str(phone):
                    results.append(record)
                    break

        return results

    def smart_search(self, search_term: str, limit: int = 5) -> list:
        """
        Smart search that finds contacts even with typos and suggests contacts
          as the user types.
        Args:
            search_term (str): The term to search for in the contact names and
              phone numbers.
            limit (int): The maximum number of suggestions to return.
            Returns:
            list: A list of `Record` instances that match the search term with
              fuzzy matching.
        """
        search_term = search_term.lower()
        names = [record.name.value for record in self.data.values()]
        phone_numbers = [
            (str(phone), record.name.value)
            for record in self.data.values()
            for phone in record.phones
        ]

        # Get fuzzy matches for names
        name_matches = process.extract(search_term, names, limit=limit)
        matched_names = [
            match[0] for match in name_matches if match[1] >= 70
        ]  # 70% similarity threshold

        # Get matches for phone numbers
        phone_matches = [
            name for phone, name in phone_numbers if search_term in phone
        ]

        # Combine name and phone matches
        matched_names.extend(phone_matches)
        matched_names = list(set(matched_names))  # Remove duplicates

        results = []
        for name in matched_names:
            record = self.data.get(name.lower())  # Fetch the Record object
            if record:  # Ensure that it's a valid Record object
                results.append(record)

        # Return just the list of Record objects
        return results

    @staticmethod
    def display_contacts(
        contacts: List[Record],
        search_term: str = "",
        field: str = ""
    ) -> str:
        """
        Displays a list of contacts in a formatted table.

        Args:
            contacts (List[Record]): A list of Record objects to be displayed.
            search_term (str, optional): The search term used to filter the
            contacts.
            field (str, optional): The field to be searched.

        Returns:
            str: A string representation of the formatted table or empty
            message.
        """
        headers = ["Name", "Phones", "Birthday", "Address", "Email"]
        table = []
        for contact in contacts:
            name = wrap_text(str(contact.name), width=20)
            if search_term and not field or field == "name":
                name = highlight_term(name, search_term)
            phones = "\n".join(map(str, contact.phones))
            if search_term and not field or field == "phones":
                phones = highlight_term(phones, search_term)
            table.append([
                name if contact.name else "-",
                phones if contact.phones else "-",
                str(contact.birthday) if contact.birthday else "-",
                (wrap_text(str(contact.address), width=40)
                    if contact.address else "-"),
                str(contact.email) if contact.email else "-",
            ])

        return display_table(headers, table)

"""
Address book module.
"""

from typing import List
from collections import UserDict
from datetime import datetime
from fuzzywuzzy import fuzz
from .record import Record
from ..helpers.colors import warning
from ..helpers.display import wrap_text, display_table, highlight_term
from ..settings.app_settings import app_settings


class AddressBook(UserDict):
    """
    Address book class which holds records.
    """

    def __init__(self) -> None:
        super().__init__()
        self.language = "en"
        self.date_str_format = "DD.MM.YYYY"

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
                app_settings.get_validation_errors()["duplicate_name"]
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
            app_settings.get_validation_errors()["name_not_found"]
            .format(contact_name)
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
                app_settings.get_validation_errors()["name_not_found"]
                .format(contact_name)
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
            str: A formatted table of upcoming birthdays.
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
            [date.strftime(app_settings.date_format), name]
            for date, name in sorted(upcoming_birthdays.items())
        ]

        if short:
            return (
                app_settings.get_info_messages()["upcoming_birthdays"]
                .format(len(sorted_birthdays), days)
                if sorted_birthdays else
                app_settings.get_info_messages()["no_birthdays"].format(days)
            )
        if not sorted_birthdays:
            return warning(
                app_settings.get_info_messages()["no_birthdays"].format(days)
            )

        headers = (
            ["Congratulation Date", "Name"]
            if app_settings.language == "en" else
            ["Дата Привітання", "Ім'я"]
        )
        return display_table(headers, sorted_birthdays)

    def smart_search(self, search_term: str) -> list:
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
        names = list(self.data)
        phone_numbers = [
            (str(phone), name)
            for name, record in self.data.items()
            for phone in record.phones
        ]

        matched_names = {}

        for name in names:
            if search_term in name:
                matched_names[name] = name.count(search_term) * 100
            else:
                match = fuzz.partial_ratio(search_term, name)
                if match >= 70:
                    matched_names[name] = match

        for phone, name in phone_numbers:
            if search_term in phone:
                matched_names[name] = (
                    matched_names.get(name, 0)
                    + phone.count(search_term) * 100
                )
            else:
                match = fuzz.ratio(search_term, phone)
                if match >= 70:
                    matched_names[name] = matched_names.get(name, 0) + match

        sorted_names = sorted(
            matched_names.items(),
            key=lambda x: x[1],
            reverse=True
        )

        results = []
        for name, _ in sorted_names:
            record = self.find(name)
            results.append(record)

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
            str: A string representation of the formatted table.
        """
        headers = (
            ["Name", "Phones", "Birthday", "Address", "Email"]
            if app_settings.language == "en" else
            ["Ім'я", "Телефони", "День народження", "Адреса",
             "Електронна пошта"])
        table = []
        for contact in contacts:
            name = wrap_text(str(contact.name), width=20)
            if search_term and not field or field == "name":
                name = highlight_term(name, search_term)

            if search_term and not field or field == "phones":
                phones = "\n".join([
                    highlight_term(str(phone), search_term)
                    for phone in contact.phones
                ])
            else:
                phones = "\n".join(map(str, contact.phones))
            table.append([
                name,
                phones if contact.phones else "-",
                str(contact.birthday) if contact.birthday else "-",
                (wrap_text(str(contact.address), width=30)
                    if contact.address else "-"),
                str(contact.email) if contact.email else "-",
            ])

        return display_table(headers, table)

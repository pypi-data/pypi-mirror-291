"""
Record module.
"""

from typing import List, Optional
from .name import Name
from .phone import Phone
from .birthday import Birthday
from .address import Address
from .email import Email
from ..constants.validation import validation_errors


class Record:
    """
    Class representing a contact in the address book.

    Attributes:
        name (Name): The name of the contact.
        phones (List[Phone]): The list of phone numbers in the contact.
        birthday (Birthday | None): The birthday of the contact.
        address (Address | None): The address of the contact.
        email (Email | None): The email address of the contact.
    """

    def __init__(self, contact_name: str) -> None:
        """
        Initializes a new Record instance.

        Args:
            contact_name (str): The name of the contact.
        """
        self.name = Name(contact_name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None
        self.email: Optional[Email] = None
        self.address: Optional[Address] = None

    def add_phone(self, phone: str) -> None:
        """
        Adds a new phone number to the record.

        Args:
            phone (str): The phone number to add.

        Raises:
            ValueError: If the phone number already exists in the record.
        """
        new_phone = Phone(phone)
        if new_phone in self.phones:
            raise ValueError(
                validation_errors["duplicate_phone"].format(phone)
            )
        self.phones.append(new_phone)

    def remove_phone(self, phone: str) -> None:
        """
        Removes a phone number from the list of phones in the `Record`
        instance.

        Args:
            phone (str): The phone number to remove.

        Raises:
            ValueError: If the phone number is not found in the list of phones.
        """
        phone_to_remove = Phone(phone)
        if phone_to_remove in self.phones:
            self.phones.remove(phone)
        else:
            raise ValueError(
                validation_errors["phone_not_found"].format(phone)
            )

    def add_birthday(self, birthday: str) -> None:
        """
        Adds a birthday to the record.

        Args:
            birthday (str): The birthday to be added.
        """
        self.birthday = Birthday(birthday)

    def remove_birthday(self) -> None:
        """
        Removes the birthday from the record.
        """
        self.birthday = None

    def add_address(self, address: str) -> None:
        """
        Adds an address to the record.

        Args:
            address (str): The address to be added.
        """
        self.address = Address(address)

    def remove_address(self) -> None:
        """
        Removes the address from the record.

        Returns:
            None
        """
        self.address = None

    def add_email(self, email: str) -> None:
        """
        Adds an email address to the record.

        Args:
            email (str): The email address to be added.
        """
        self.email = Email(email)

    def remove_email(self) -> None:
        """
        Removes the email address from the record.
        """
        self.email = None

"""
Phone field module.
"""

import re
from typing import Union
from ..constants.validation import PHONE_PATTERN, validation_errors


class Phone:
    """
    Class representing a phone field.
    """

    def __init__(self, phone: str) -> None:
        """
        Initialize a phone field.

        Args:
            phone (str): The phone number.

        Raises:
            ValueError: If the phone number does not consist of 10 digits.
        """
        if not re.match(PHONE_PATTERN, phone):
            raise ValueError(validation_errors["invalid_phone"])
        self.value = phone

    def __repr__(self) -> str:
        """
        Return the string representation of the phone field.

        Returns:
            str: The string representation of the phone field.
        """
        return self.value

    def __eq__(self, other: Union[str, "Phone"]) -> bool:
        """
        Checks if two Phone instances are equal.

        Args:
            other (Phone): The Phone instance to compare with.

        Returns:
            bool: True if the Phone instances are equal, False otherwise.
        """
        if isinstance(other, Phone):
            return self.value == other.value
        return self.value == other

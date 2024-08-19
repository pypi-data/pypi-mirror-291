"""
Name field module.
"""

from ..constants.validation import (
    NAME_MIN_LENGTH,
    NAME_MAX_LENGTH,
    validation_errors
)


class Name:
    """
    Class representing a name field.
    """

    def __init__(self, contact_name: str) -> None:
        """
        Initialize a name field.

        Args:
            contact_name (str): The name of the contact.

        Raises:
            ValueError: If the name is not valid.
        """
        if not NAME_MIN_LENGTH <= len(contact_name) <= NAME_MAX_LENGTH:
            raise ValueError(validation_errors["invalid_name"])
        self.value = contact_name.strip()

    def __str__(self) -> str:
        """
        Return the string representation of the name field.

        Returns:
            str: The string representation of the name field.
        """
        return self.value

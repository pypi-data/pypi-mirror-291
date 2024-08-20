"""
Address field module.
"""

from ..settings.app_settings import app_settings
from ..constants.values import ADDRESS_MIN_LENGTH, ADDRESS_MAX_LENGTH


class Address:
    """
    Class representing an address field.
    """

    def __init__(self, address: str) -> None:
        """
        Initialize an address field.

        Args:
            address (str): The address.

        Raises:
            ValueError: If the address does not meet the validation criteria.
        """
        if not ADDRESS_MIN_LENGTH <= len(address) <= ADDRESS_MAX_LENGTH:
            raise ValueError(
                app_settings.get_validation_errors()["invalid_address"]
            )
        self.value = address

    def __str__(self) -> str:
        """
        Return the string representation of the address field.

        Returns:
            str: The string representation of the address field.
        """
        return self.value

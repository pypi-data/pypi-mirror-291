"""
Email field module.
"""

import re
from ..settings.app_settings import app_settings
from ..constants.values import EMAIL_PATTERN


class Email:
    """
    Class representing an email field.
    """

    def __init__(self, email: str) -> None:
        """
        Initialize an email field.

        Args:
            email (str): The email address.

        Raises:
            ValueError: If the email does not meet the validation criteria.
        """
        if not re.match(EMAIL_PATTERN, email):
            raise ValueError(
                app_settings.get_validation_errors()["invalid_email"]
            )
        self.value = email

    def __str__(self) -> str:
        """
        Return the string representation of the address field.

        Returns:
            str: The string representation of the address field.
        """
        return self.value

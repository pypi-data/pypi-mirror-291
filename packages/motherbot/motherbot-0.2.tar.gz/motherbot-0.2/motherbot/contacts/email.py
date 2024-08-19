"""
Email field module.
"""

import re
from ..constants.validation import EMAIL_PATTERN, validation_errors


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
            raise ValueError(validation_errors["invalid_email"])
        self.value = email

    def __str__(self) -> str:
        """
        Return the string representation of the address field.

        Returns:
            str: The string representation of the address field.
        """
        return self.value

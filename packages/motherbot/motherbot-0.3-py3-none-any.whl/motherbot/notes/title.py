"""
Title field module.
"""

from ..settings.app_settings import app_settings
from ..constants.values import TITLE_MIN_LENGTH, TITLE_MAX_LENGTH


class Title:
    """
    Class representing a title field.
    """

    def __init__(self, value: str) -> None:
        """
        Initialize a title field.

        Args:
            value (str): The title of the note.

        Raises:
            ValueError: If the value is empty.
        """
        value = value.strip()
        if len(value) < TITLE_MIN_LENGTH or len(value) > TITLE_MAX_LENGTH:
            raise ValueError(
                app_settings.get_validation_errors()["invalid_title"]
            )
        self.value = value

    def __str__(self):
        """
        Return the string representation of the title field.

        Returns:
            str: The string representation of the title field.
        """
        return self.value

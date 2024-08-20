"""
Text field module
"""

from ..settings.app_settings import app_settings
from ..constants.values import TEXT_MAX_LENGTH


class Text:
    """
    Class representing a tag field.
    """

    def __init__(self, value: str) -> None:
        """
        Initialize a text field.

        Args:
            value (str): The text of the note.

        Raises:
            ValueError: If the value is empty.
        """
        value = value.strip()
        if not value or len(value) > TEXT_MAX_LENGTH:
            raise ValueError(
                app_settings.get_validation_errors()["invalid_text"]
            )
        self.value = value

    def __str__(self) -> str:
        """
        Return the string representation of the text field.

        Returns:
            str: The string representation of the text field.
        """

        return self.value

"""
Tag field module
"""

from ..settings.app_settings import app_settings
from ..constants.values import TAG_MIN_LENGTH, TAG_MAX_LENGTH


class Tag:
    """
    Class representing a tag field.
    """

    def __init__(self, value: str) -> None:
        """
        Initialize a tag field.

        Args:
            value (str): The tag of the note.

        Raises:
            ValueError: If the value is empty.
        """
        value = value.lower().strip()
        if len(value) < TAG_MIN_LENGTH or len(value) > TAG_MAX_LENGTH:
            raise ValueError(
                app_settings.get_validation_errors()["invalid_tag"]
            )
        self.value = value

    def __str__(self) -> str:
        """
        Return the string representation of the tag field.

        Returns:
            str: The string representation of the tag field.
        """

        return f"#{self.value}"

    def __eq__(self, other) -> bool:
        """
        Checks if Tag instance equal to other instance or str.

        Args:
            other (Tag): The Tag instance to compare with.

        Returns:
            bool: True if the Tag instances are equal, False otherwise.
        """
        if isinstance(other, Tag):
            return self.value == other.value
        return self.value == other

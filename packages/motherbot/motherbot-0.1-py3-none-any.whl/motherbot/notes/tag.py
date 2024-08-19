"""
Tag field module
"""


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
        if not value.strip():
            raise ValueError("Tag cannot be empty")
        if len(value.strip()) < 2 or len(value.strip()) > 16:
            raise ValueError("Tag must be min 2 symbols and max 16 symbols")
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

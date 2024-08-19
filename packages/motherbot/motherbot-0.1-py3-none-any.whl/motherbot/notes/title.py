"""
Title field module.
"""


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
        if not value.strip():
            raise ValueError("Title cannot be empty")
        if len(value.strip()) < 2:
            raise ValueError("Title must be at least 2 symbols")
        self.value = value

    def __str__(self):
        """
        Return the string representation of the title field.

        Returns:
            str: The string representation of the title field.
        """
        return self.value

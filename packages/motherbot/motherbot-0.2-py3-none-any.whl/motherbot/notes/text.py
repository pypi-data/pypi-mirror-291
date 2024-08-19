"""
Text field module
"""


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
        if not value.strip():
            raise ValueError("Text cannot be empty")
        if len(value.strip()) > 200:
            raise ValueError("Text must be max 200 symbols")
        self.value = value

    def __str__(self) -> str:
        """
        Return the string representation of the text field.

        Returns:
            str: The string representation of the text field.
        """

        return self.value

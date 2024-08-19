"""
CreatedOn module.
"""

from datetime import datetime


class CreatedOn:
    """
    Class representing the creation date of an object.

    Attributes:
        created_on (datetime): The datetime object representing when the instance was created.
    """

    def __init__(self) -> None:
        """
        Initializes a new CreatedOn instance with the current date and time.

        Returns:
            None
        """
        self.created_on = datetime.now()

    def __str__(self) -> str:
        """
        Returns a string representation of the creation date.

        Returns:
            str: The creation date formatted as DD.MM.YYYY.
        """
        return self.created_on.strftime("%d.%m.%Y")

"""
Reminder module.
"""

from datetime import datetime
from ..settings.app_settings import app_settings


class Reminder:
    """
    Class representing a reminder for a specific date.

    Attributes:
        value (datetime): The datetime object representing the reminder date.
    """

    def __init__(self, reminder: str) -> None:
        """
        Initializes a new Reminder instance and sets the reminder date.

        Args:
            remind_date (str): The reminder date in the format DD.MM.YYYY.

        Raises:
            ValueError: If the date format is invalid or the date is not in
            the future.
        """
        try:
            reminder_date = datetime.strptime(
                reminder,
                app_settings.date_format
            ).date()
        except ValueError as exc:
            raise ValueError(
                app_settings.get_validation_errors()["invalid_date"]
                .format(app_settings.date_str_format)
            ) from exc

        if reminder_date <= datetime.now().date():
            raise ValueError(
                app_settings.get_validation_errors()["invalid_reminder"]
            )
        self.value = reminder_date

    def __str__(self) -> str:
        """
        Returns a string representation of the reminder date.

        Returns:
            str: The reminder date as a string in the format DD.MM.YYYY.
        """
        return self.value.strftime(app_settings.date_format)

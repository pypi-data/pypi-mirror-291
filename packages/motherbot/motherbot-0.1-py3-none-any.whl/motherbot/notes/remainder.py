"""
Reminder module.
"""

from datetime import datetime, timedelta


class Reminder:
    """
    Class representing a reminder for a specific date.

    Attributes:
        value (datetime): The datetime object representing the reminder date.
    """

    def __init__(self, remind_date: str) -> None:
        """
        Initializes a new Reminder instance and sets the reminder date.

        Args:
            remind_date (str): The reminder date in the format DD.MM.YYYY.

        Raises:
            ValueError: If the date format is invalid or the date is not in
            the future.
        """
        self.set_reminder(remind_date)

    def set_reminder(self, new_date: str) -> None:
        """
        Sets or updates the reminder date.

        Args:
            new_date (str): The new reminder date in the format DD.MM.YYYY.

        Raises:
            ValueError: If the date format is invalid or the date is not in
            the future.
        """
        try:
            remind_datetime = datetime.strptime(new_date, "%d.%m.%Y").date()
        except ValueError as exc:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from exc

        if remind_datetime <= datetime.now().date():
            raise ValueError("Date must be greater than today")
        self.value = remind_datetime

    def is_reminder_due(self, days: int) -> bool:
        """
        Checks if the reminder is due within a specified number of days.

        Args:
            days (int): The number of days to check if the reminder is due.

        Returns:
            bool: True if the reminder is due within the specified number of
            days, False otherwise.
        """
        today = datetime.now()
        end_date = today + timedelta(days=days)
        return today <= self.value <= end_date

    def __str__(self) -> str:
        """
        Returns a string representation of the reminder date.

        Returns:
            str: The reminder date as a string in the format DD.MM.YYYY.
        """
        return self.value.strftime("%d.%m.%Y")

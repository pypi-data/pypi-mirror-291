"""
Birthday field module.
"""

from datetime import datetime
from ..constants.validation import DATE_FORMAT, validation_errors


class Birthday:
    """
    Class representing a birthday field.
    """

    def __init__(self, value: str) -> None:
        try:
            birthday = datetime.strptime(value, DATE_FORMAT).date()
            if birthday > datetime.now().date():
                raise ValueError(validation_errors["future_birthday"])
            self.value = birthday
        except ValueError as exc:
            raise ValueError(validation_errors["invalid_birthday"]) from exc

    def __str__(self) -> str:
        return self.value.strftime(DATE_FORMAT)

"""
Birthday field module.
"""

from datetime import datetime
from ..settings.app_settings import app_settings


class Birthday:
    """
    Class representing a birthday field.
    """

    def __init__(self, value: str) -> None:
        try:
            birthday = datetime.strptime(
                value,
                app_settings.date_format
            ).date()
            if birthday > datetime.now().date():
                raise ValueError(
                    app_settings.get_validation_errors()["future_birthday"]
                )
            self.value = birthday
        except ValueError as exc:
            raise ValueError(
                app_settings.get_validation_errors()["invalid_date"]
                .format(app_settings.date_str_format)
            ) from exc

    def __str__(self) -> str:
        return self.value.strftime(app_settings.date_format)

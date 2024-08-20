from ..constants.commands import (
    command_names_en,
    command_names_ua,
    command_descriptions_en,
    command_descriptions_ua,
)
from ..constants.info_messages import info_messages_en, info_messages_ua
from ..constants.questions import questions_en, questions_ua
from ..constants.validation import validation_errors_en, validation_errors_ua


class AppSettings:
    def __init__(self) -> None:
        """
        Initializes a new AppSettings instance with default settings.

        Sets the language to English, date format to DD.MM.YYYY, and available
        languages and date formats.
        """
        self._language = "en"
        self._date_format = "%d.%m.%Y"
        self._date_str_format = "DD.MM.YYYY"
        self._available_languages = ["en", "ua"]
        self._available_date_formats = {
            "DD.MM.YYYY": "%d.%m.%Y",
            "MM/DD/YYYY": "%m/%d/%Y",
            "YYYY-MM-DD": "%Y-%m-%d",
        }

    @property
    def language(self) -> str:
        """
        Returns the current language.
        """
        return self._language

    @language.setter
    def language(self, value: str) -> None:
        """
        Sets the current language.
        """
        if value in self._available_languages:
            self._language = value
        else:
            raise ValueError(
                f"Language must be one of: "
                f"{", ".join(self._available_languages)}"
                if self.language == "en"
                else
                f"Мова має бути однією з: "
                f"{', '.join(self._available_languages)}"
            )

    @property
    def date_format(self) -> str:
        """
        Returns the current date format.
        """
        return self._date_format

    @property
    def date_str_format(self) -> str:
        """
        Returns the current date string format.
        """
        return self._date_str_format

    @date_format.setter
    def date_format(self, key) -> None:
        """
        Sets the current date format.
        """
        if key in self._available_date_formats:
            self._date_format = self._available_date_formats[key]
            self._date_str_format = key
        else:
            raise ValueError(
                f"Date format must be one of: "
                f"{", ".join(self._available_date_formats.keys())}"
                if self.language == "en"
                else
                f"Формат дати має бути одним з: "
                f"{', '.join(self._available_date_formats.keys())}"
            )

    def list_languages(self) -> list:
        """
        Returns the list of available languages.
        """
        return self._available_languages

    def list_date_formats(self) -> list:
        """
        Returns the list of available date formats.
        """
        return list(self._available_date_formats.keys())

    def get_command_names(self) -> dict:
        """
        Returns the command names dictionary based on the current language.
        """
        return command_names_ua if self.language == "ua" else command_names_en

    def get_command_descriptions(self) -> dict:
        """
        Returns the command descriptions dictionary based on the current
        language.
        """
        return (
            command_descriptions_ua if self.language == "ua"
            else command_descriptions_en
        )

    def get_info_messages(self) -> dict:
        """
        Returns the info messages dictionary based on the current language.
        """
        return info_messages_ua if self.language == "ua" else info_messages_en

    def get_questions(self) -> dict:
        """
        Returns the questions dictionary based on the current language.
        """
        return questions_ua if self.language == "ua" else questions_en

    def get_validation_errors(self) -> dict:
        """
        Returns the validation errors dictionary based on the current language.
        """
        return (
            validation_errors_ua if self.language == "ua"
            else validation_errors_en
        )

    def __str__(self) -> str:
        """
        Returns a string representation of the AppSettings instance.
        """
        return (f"Language: {self.language}\n"
                f"Date Format: {self.date_format}")


app_settings = AppSettings()

"""
NotesBook module.
"""
from datetime import datetime
from collections import UserDict
from fuzzywuzzy import fuzz
from .note import Note
from ..helpers.display import display_table, highlight_term, wrap_text
from ..settings.app_settings import app_settings


class NotesBook(UserDict):
    """
    Class representing a collection of notes.
    """

    def add_note(self, note: Note) -> None:
        """
        Adds a new note to the collection.

        Args:
            note (Note): The note to be added.

        Raises:
            ValueError: If a note with the same title already exists.
        """
        normalized_title = note.title.value.lower()
        if normalized_title in self.data:
            raise ValueError(
                app_settings.get_validation_errors()["duplicate_title"]
                .format(note.title.value)
            )
        self.data[normalized_title] = note

    def delete(self, note_title: str) -> None:
        """
        Deletes a note from the collection by its title.

        Args:
            note_title (str): The title of the note to delete.

        Raises:
            ValueError: If the note with the specified title is not found.
        """
        normalized_note_title = note_title.lower()
        if normalized_note_title not in self.data:
            raise ValueError(
                app_settings.get_validation_errors()["title_not_found"]
                .format(note_title)
            )
        del self.data[normalized_note_title]

    def find(self, note_title: str) -> Note:
        """
        Finds and returns a note by its title.

        Args:
            note_title (str): The title of the note to find.

        Returns:
            Note: The note object with the specified title.

        Raises:
            ValueError: If the note with the specified title is not found.
        """
        normalized_note_title = note_title.lower()
        if normalized_note_title in self.data:
            return self.data[normalized_note_title]
        raise ValueError(
            app_settings.get_validation_errors()["title_not_found"]
            .format(note_title)
        )

    def smart_search(self, search_term: str) -> list:
        """
        Smart search that finds contacts even with typos and suggests contacts
          as the user types.

        Args:
            search_term (str): The term to search for in the contact names and
              phone numbers.
            limit (int): The maximum number of suggestions to return.
            Returns:
            list: A list of `Record` instances that match the search term with
              fuzzy matching.
        """
        search_term = search_term.lower()
        titles = list(self.data)
        tags = [
            (str(tag), name)
            for name, note in self.data.items()
            for tag in note.tags
        ]

        matched_titles = {}

        for title in titles:
            if search_term in title:
                matched_titles[title] = title.count(search_term) * 100
            else:
                match = fuzz.partial_ratio(search_term, title)
                if match >= 70:
                    matched_titles[title] = match

        for tag, title in tags:
            if search_term in tag:
                matched_titles[title] = (
                    matched_titles.get(title, 0)
                    + tag.count(search_term) * 100
                )
                continue
            match = fuzz.ratio(search_term, tag)
            if match >= 70:
                matched_titles[title] = matched_titles.get(title, 0) + match

        sorted_titles = sorted(
            matched_titles.items(),
            key=lambda x: x[1],
            reverse=True
        )

        results = []
        for title, _ in sorted_titles:
            note = self.find(title)
            results.append(note)

        return results

    def upcoming_reminders(self, days: int, short: bool = False) -> list:
        """
        Calculate upcoming reminders within a number of days.

        Args:
            days (int): The number of days to check for upcoming reminders.
            short (bool, optional): If True, the output will be shortened.

        Returns:
            list: A list of notes with upcoming reminders within the given
            number of days.
        """
        today = datetime.today().date()
        upcoming_reminders = {}

        for note in self.data.values():
            if note.reminder is None or note.reminder.value < today:
                continue
            days_until_reminder = (note.reminder.value - today).days
            if 0 <= days_until_reminder <= days:
                upcoming_reminders[note.reminder.value] = note
        sorted_reminders = dict(sorted(upcoming_reminders.items()))

        if short:
            return (
                app_settings.get_info_messages()["reminders"]
                .format(len(sorted_reminders), days)
                if sorted_reminders else
                app_settings.get_info_messages()["no_reminders"].format(days)
            )

        return sorted_reminders.values()

    @staticmethod
    def display_notes(
        notes: list[Note],
        search_term: str = "",
        field: str = ""
    ) -> str:
        """
        Displays a list of notes in a table format.

        Args:
            notes (list[Note]): A list of notes to display.
            search_term (str, optional): The search term used to filter the
            contacts.
            field (str, optional): The field to be searched.

        Returns:
            str: A formatted table of notes.
        """
        headers = (
            ["Title", "Text", "Tags", "Created On", "Reminder"]
            if app_settings.language == "en" else
            ["Назва", "Текст", "Теги", "Дата Створення", "Нагадування"]
        )
        table = []
        for note in notes:
            title = wrap_text(str(note.title), width=20)
            if search_term and not field or field == "title":
                title = highlight_term(title, search_term)
            tags = wrap_text(" ".join(map(str, note.tags)), width=15)
            if search_term and not field or field == "tags":
                tags = highlight_term(tags, search_term)
            table.append([
                title,
                wrap_text(str(note.text), width=40) if note.text else "-",
                tags if note.tags else "-",
                str(note.created_on),
                str(note.reminder) if note.reminder else "-"
            ])

        return display_table(headers, table)

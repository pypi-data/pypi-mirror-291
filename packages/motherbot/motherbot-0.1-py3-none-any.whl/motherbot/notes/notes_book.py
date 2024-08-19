"""
NotesBook module.
"""
from datetime import datetime
from collections import UserDict
from .note import Note


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
            raise ValueError(f"Note {note.title.value} already exists")
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
            raise ValueError(f"Note {note_title} not found")
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
        raise ValueError(f"Note {note_title} not found")

    def search_notes_by_tag(self, tag: str) -> list[Note]:
        """
        Searches for notes containing a specific tag.

        Args:
            tag (str): The tag to search for.

        Returns:
            list[Note]: A list of notes containing the specified tag.
        """
        tag_normalized = tag.strip().lower()
        return [
            note for note in self.data.values()
            if any(t.value in tag_normalized for t in note.tags)
        ]

    def search_notes_by_title(self, title: str) -> list[Note]:
        """
        Searches for notes by title.

        Args:
            title (str): The title to search for.

        Returns:
            list[Note]: A list of notes containing the title.
        """
        title_normalized = title.strip().lower()
        return [
            note for note in self.data.values()
            if title_normalized in note.title.value.lower()
        ]

    def sort_notes_by_tag(self, tag: str) -> list[Note]:
        """
        Sorts notes by the presence of a specific tag.

        Args:
            tag (str): The tag to sort by.

        Returns:
            list[Note]: A list of notes sorted by the presence of the
            specified tag.
        """
        tag_normalized = tag.strip().lower()
        tagged_notes = [note for note in self.data.values() if any(
            t.value.lower() == tag_normalized for t in note.tags)]
        return sorted(tagged_notes, key=lambda note: note.title.value.lower())

    def sort_notes_by_title(self, ascending: bool = True) -> list[Note]:
        """
        Sorts all notes in the collection by their title.

        Args:
            ascending (bool): If True, sorts the notes in ascending order.
                            If False, sorts the notes in descending order.

        Returns:
            list[Note]: A list of notes sorted by their title.
        """
        return sorted(
            self.data.values(),
            key=lambda note: note.title.value.lower(),
            reverse=not ascending
        )

    @property
    def all_tags(self) -> set:
        """
        Returns a set of all unique tags used in the notes.

        Returns:
            set: A set of unique tags.
        """
        return {tag.value for note in self.data.values() for tag in note.tags}

    def upcoming_reminders(self, days: int) -> list:
        """
        Calculate upcoming reminders within a number of days.

        Args:
            days (int): The number of days to check for upcoming reminders.

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

        return sorted_reminders.values()

"""
Note module.
"""

from typing import List
from .title import Title
from .text import Text
from .tag import Tag
from .remainder import Reminder
from .created_on import CreatedOn
from ..settings.app_settings import app_settings


class Note:
    """
    Class representing a note in the notes book.

    Attributes:
        title (Title): The title of the note.
        text (str): The text of the note.
        tags (List[Tag]): The list of tags in the note.
        created_on (CreatedOn): The created_on of the note.
        reminder (Reminder): The reminder of the note.
    """

    def __init__(self, title: str) -> None:
        """
        Initializes a new Note instance.

        Args:
            title (str): The title of the note.

        Returns:
            None
        """
        self.title: Title = Title(title)
        self.text: Text | None = None
        self.tags: List[Tag] = []
        self.created_on: CreatedOn = CreatedOn()
        self.reminder: Reminder | None = None

    def add_text(self, text: str) -> None:
        """
        Adds text to the note.

        Args:
            text (str): The text to add.

        Returns:
            None
        """
        self.text = Text(text)

    def add_tags(self, tags: str) -> None:
        """
        Adds tags to the note. Tags are separated by spaces.

        Args:
            tags (str): A string of tags separated by spaces.

        Returns:
            None
        """

        tag_list = tags.split()

        for tag in tag_list:
            if tag.lower() not in self.tags:
                self.tags.append(Tag(tag))

    def remove_tag(self, tag: str):
        """
        Removes a tag from the list of tags in the `Note`
        instance.

        Args:
            tag (str): The tag to remove.

        Raises:
            ValueError: If the tag is not found in the list of tags.

        Returns:
            None
        """
        tag_to_remove = Tag(tag)
        if tag_to_remove in self.tags:
            self.tags.remove(tag)
        else:
            raise ValueError(
                app_settings.get_validation_errors()["tag_not_found"]
                .format(tag)
            )

    def set_reminder(self, remind_date: str) -> None:
        """
        Sets reminder to the note.

        Args:
            remind_date (str): The remind_date to add.

        Returns:
            None
        """
        self.reminder = Reminder(remind_date)

    def remove_text(self):
        """
        Removes the text from the note.

        Returns:
            None
        """
        self.text = None

    def remove_reminder(self):
        """
        Removes the reminder from the note.

        Returns:
            None
        """
        self.reminder = None

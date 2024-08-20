"""
Suggests the closest matching command in case incorrect input.
"""

from fuzzywuzzy import process


def suggest_command(user_command: str, commands: list[str]) -> str | None:
    """
    Suggests the closest matching command in case incorrect input.
    """
    similar_command, match = process.extractOne(user_command, commands)

    if match >= 50:
        return similar_command
    return None

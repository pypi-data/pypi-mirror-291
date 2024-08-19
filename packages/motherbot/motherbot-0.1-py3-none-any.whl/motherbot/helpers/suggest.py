import difflib


def suggest_command(user_command: str, commands: list[str]) -> list:
    """
    Suggests the closest matching command in case incorrect input.
    """
    closest_matches = difflib.get_close_matches(
        user_command.lower(), commands, n=2, cutoff=0.6
    )

    if closest_matches:
        return closest_matches
    return None

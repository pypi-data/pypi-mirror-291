"""
Colors module.
"""

from colorama import Fore, Style, Back, init
init(autoreset=True)


# Colors for ********************* Text *********************
def green(text: str) -> str:
    """
    Returns the input text in green color.

    Args:
        text (str): The text to be colored.

    Returns:
        str: The input text in green color.
    """
    return Fore.GREEN + text + Fore.RESET


def blue(text: str) -> str:
    """
    Returns the input text in blue color.

    Args:
        text (str): The text to be colored.

    Returns:
        str: The input text in blue color.
    """
    return Fore.BLUE + text + Fore.RESET


def yellow(text: str) -> str:
    """
    Returns the input text in yellow color.

    Args:
        text (str): The text to be colored.

    Returns:
        str: The input text in yellow color.
    """
    return Fore.YELLOW + text + Fore.RESET


def red(text: str) -> str:
    """
    Returns the input text in red color.

    Args:
        text (str): The text to be colored.

    Returns:
        str: The input text in red color.
    """
    return Fore.RED + text + Fore.RESET


def gray(text: str) -> str:
    """
    Returns the input text in gray color.

    Args:
        text: The text to be colored.

    Returns:
        str: The input text in gray color.
    """
    gray_color = "\033[38;5;242m"
    reset = "\033[0m"

    return f"{gray_color}{text}{reset}"


# Colors for ********************* BackGround *********************
def success(text: str) -> str:
    """
    Returns the input text with a green background and white foreground.

    Args:
        text: The text to be styled.

    Returns:
        str: The styled text.
    """
    return Fore.WHITE + Back.GREEN + text + Style.RESET_ALL


def warning(text: str) -> str:
    """
    Returns the input text with a yellow background and white foreground.

    Args:
        text (str): The text to be styled.

    Returns:
        str: The styled text.
    """
    return Fore.WHITE + Back.YELLOW + text + Style.RESET_ALL


def danger(text: str) -> str:
    """
    Returns the input text with a red background and white foreground.

    Args:
        text (str): The text to be styled.

    Returns:
        str: The styled text.
    """
    return Fore.WHITE + Back.RED + text + Style.RESET_ALL

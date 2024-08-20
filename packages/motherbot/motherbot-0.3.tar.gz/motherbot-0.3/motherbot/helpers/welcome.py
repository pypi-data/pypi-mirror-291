"""
Prints a title with a specified font size and color.
"""

import pyfiglet


def print_title(title: str, color_func, font_size: str = 'standart'):
    """
    Prints a title with a specified font size and color.

    Args:
        title (str): The title to be printed.
        color_func: A function that takes a string and returns a colored
        string.
        font_size (str, optional): The font size of the title. Defaults to
        'standart'.

    Returns:
        None
    """
    font_map = {
        'small': 'slant',
        'medium': 'standard',
        'large': 'big'
    }
    font_name = font_map.get(font_size, 'standard')
    ascii_title = pyfiglet.figlet_format(title, font=font_name)
    print(color_func(ascii_title))

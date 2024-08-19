"""
Colors module.
"""

from colorama import Fore, Back, Style, init

# Initialize Colorama
init(autoreset=True)


# Colors for ********************* TEXT *********************
def green(text):
    return Fore.GREEN + text + Fore.RESET


def blue(text):
    return Fore.BLUE + text + Fore.RESET


def yellow(text):
    return Fore.YELLOW + text + Fore.RESET


def red(text):
    return Fore.RED + text + Fore.RESET

  
def dim(text):
    return Style.DIM + text + Style.RESET_ALL



# Colors for ********************* BackGround *********************
def success(text):
    return Fore.WHITE + Back.GREEN + text


def warning(text):
    return Fore.WHITE + Back.YELLOW + text


def danger(text):
    return Fore.WHITE + Back.RED + text

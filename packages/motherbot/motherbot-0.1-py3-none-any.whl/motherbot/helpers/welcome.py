import pyfiglet


def print_title(title: str, color_func, font_size: str = 'standart'):
    font_map = {
        'small': 'slant',
        'medium': 'standard',
        'large': 'big'
    }
    font_name = font_map.get(font_size, 'standard')
    ascii_title = pyfiglet.figlet_format(title, font=font_name)
    print(color_func(ascii_title))

### Print colored text to console (a more complete version exists: print_color_styled)

def print_colored(text, color='', background=''):
    """Print colored text to console using ANSI escape codes.
    
    Args:
        text: The text to print
        color: Foreground color name (default='')
            Options: red, green, yellow, blue, magenta/purple, cyan, white, black
        background: Background color name (default='')
            Options: red, green, yellow, blue, magenta/purple, cyan, white, black
    """
    colors = {
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'purple': '\033[35m', # alias magenta
        'cyan': '\033[36m',
        'white': '\033[37m',
    }
    
    backgrounds = {
        'black': '\033[40m',
        'red': '\033[41m',
        'green': '\033[42m',
        'yellow': '\033[43m',
        'blue': '\033[44m',
        'magenta': '\033[45m',
        'purple': '\033[45m', # alias magenta
        'cyan': '\033[46m',
        'white': '\033[47m',
    }
    
    reset = '\033[0m'
    
    # Default to green only if nothing is specified
    if not color and not background:
        color = 'green'
    
    color_code = colors.get(color.lower(), '')
    bg_code = backgrounds.get(background.lower(), '')
    
    print(f"{color_code}{bg_code}{text}{reset}")


## Usage examples:
# print_colored("Green by default, same as color='green'")
# print_colored("Just yellow background", background='yellow')
# print_colored("White on blue", color='white', background='blue')
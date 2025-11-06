## Styled and colored prints in console

def print_styled(text, color='', background='', 
                bold=False, dim=False, italic=False, underline=False, 
                blink=False, reverse=False, strikethrough=False):
    """Print styled text to console using ANSI escape codes.

    Args:
        text: The text to print
        color: Foreground color (red, green, yellow, blue, magenta/purple, cyan, white, black)
        background: Background color (red, green, yellow, blue, magenta/purple, cyan, white, black)
        bold: Bold/bright text
        dim: Dim/faint text
        italic: Italic text
        underline: Underlined text
        blink: Blinking text
        reverse: Reverse (swap foreground/background)
        strikethrough: Strikethrough text
    """
    colors = {
        'black': '30',
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'magenta': '35',
        'purple': '35', # alias magenta
        'cyan': '36',
        'white': '37',
    }

    backgrounds = {
        'black': '40',
        'red': '41',
        'green': '42',
        'yellow': '43',
        'blue': '44',
        'magenta': '45',
        'purple': '45', # alias magenta
        'cyan': '46',
        'white': '47',
    }

    reset = '\033[0m'

    # Default to bright green only if nothing is specified
    if not color and not background and not any([bold, dim, italic, underline, blink, reverse, strikethrough]):
        color = 'green'
        bold = True

    # Build the list of codes
    codes = []
    if bold:
        codes.append('1')
    if dim:
        codes.append('2')
    if italic:
        codes.append('3')
    if underline:
        codes.append('4')
    if blink:
        codes.append('5')
    if reverse:
        codes.append('7')
    if strikethrough:
        codes.append('9')
    if color:
        codes.append(colors.get(color.lower(), ''))
    if background:
        codes.append(backgrounds.get(background.lower(), ''))

    color_code = f"\033[{';'.join(codes)}m" if codes else ''

    print(f"{color_code}{text}{reset}")


## Usage examples:
# print_styled("Bold green (default, same as color='green', bold=True)")
# print_styled("Underlined blue", color='blue', underline=True)
# print_styled("Bold underlined red", color='red', bold=True, underline=True)
# print_styled("All styles!", color='magenta', bold=True, italic=True, underline=True, strikethrough=True)
# print_styled("Just bold, no color", bold=True)
# print_styled("Reverse", reverse=True)
# print_styled("Italic cyan on yellow", color='cyan', background='yellow', italic=True)

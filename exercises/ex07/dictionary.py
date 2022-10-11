"""Sample functions using dictionaries."""

__author__ = "930605992"


def invert(a: dict[str, str]) -> dict[str, str]:
    """Swaps the keys and values of a [str, str] dictionary."""
    result: dict[str, str] = {}
    for key in a:
        if a[key] in result:
            raise KeyError("You cannot have multiple instances of the same key!")
        result[a[key]] = key
    return result
    

def favorite_color(a: dict[str, str]) -> str:
    """Returns color that appears the most in a dictionary of type [str, str] containing names and colors."""
    if a == {}:
        return ""
    color_counter: dict[str, int] = {}
    for key in a:
        if a[key] not in color_counter:
            color_counter[a[key]] = 1
        else:
            color_counter[a[key]] += 1
    colors: dict[int, str] = {}
    for color in color_counter:
        if not color_counter[color] in colors:
            colors[color_counter[color]] = color
        # else:
        #     colors[color_counter[color]] += ", " + color
    mode_num: int = 0
    for number in colors:
        if number > mode_num:
            mode_num = number
    return colors[mode_num]


def count(a: list[str]) -> dict[str, int]:
    """Returns dictionary of inputs with their frequencies given a list of strings."""
    frequencies: dict[str, int] = {}
    for num in a:
        if num not in frequencies:
            frequencies[num] = 1
        else:
            frequencies[num] += 1
    return frequencies
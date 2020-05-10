import re


# transform feet and inches to cm
def ft_and_inch_to_cm(ft_and_inch):
    if isinstance(ft_and_inch, str):
        ft = re.search('([0-9])+ft', ft_and_inch)
        ft = ft.group(1) if ft is not None else 0
        inch = re.search('([0-9])+in', ft_and_inch)
        inch = inch.group(1) if inch is not None else 0
        return int(ft) * 30.48 + int(inch) * 2.54
    return None


# cup size: a, b, c, d, dd, ddd, ... -> 1, 2, 3, 4, 5, 6, ...
def cup_size_to_ordinal(cup_size):
    if str(cup_size).replace('.', '', 1).isdigit():
        return cup_size

    cup_size = str(cup_size)
    slash_pos = cup_size.find("/")
    if slash_pos != -1:
        cup_size = cup_size[:slash_pos]

    if cup_size[0] == "a":
        return 1
    if cup_size[0] == "b":
        return 2
    if cup_size[0] == "c":
        return 3
    if cup_size[0] == "d":
        return 4 + (len(cup_size) - 1)
    return None


# length: slightly short, just right, slightly long -> -1, 0, 1
def length_to_ordinal(length):
    if length == "slightly short":
        return -1
    if length == "just right":
        return 0
    if length == "slightly long":
        return 1
    return None


# shoe width: narrow, average, wide -> -1, 0, 1
def shoe_width_to_ordinal(shoe_width):
    if shoe_width == "narrow":
        return -1
    if shoe_width == "average":
        return 0
    if shoe_width == "wide":
        return 1
    return None


# small, fit, large -> -1, 0, 1
def fit_to_ordinal(fit):
    if fit == "small":
        return -1
    if fit == "average":
        return 0
    if fit == "wide":
        return 1
    return None
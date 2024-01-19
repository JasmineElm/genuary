#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Genuary day 9 - ASCII
"""
import random
import toml

# local libraries
from helpers import svg, utils

# Load config file and set DEFAULT parameters
config = toml.load("config.toml")
DEFAULT = config["DEFAULT"]
DEFAULT.update({"PAPER_SIZE": svg.set_image_size(DEFAULT['SIZE'],
                                                 DEFAULT['PPMM'],
                                                 DEFAULT['LANDSCAPE'])})
DEFAULT.update({"DRAWABLE_AREA": svg.set_drawable_area(DEFAULT['PAPER_SIZE'],
                                                       DEFAULT['BLEED'])})
DEFAULT.update({"FILENAME": utils.create_dir(
    DEFAULT['OUTPUT_DIR']) + utils.generate_filename()})


# LOCAL VARIABLES
FONT_FAMILY = "monospace"
LOWER_CASE = [97, 122]
UPPER_CASE = [65, 90]
NUMBERS = [48, 57]
FILL = "black"
OBJECT_COUNT = 300
MIN_MAX_FONT_SIZE = [5, 400]
# LOCAL FUNCTIONS


def random_text_string(length, range_list):
    """
    Returns a random string of text.

    Returns:
        str: a random string of text.
    """
    text = ""
    for _ in range(length):
        text += chr(random.randint(*random.choice(range_list)))
    return text


def string_to_object(string, xy, font_styles):
    return f"<text x='{xy[0]}' y='{xy[1]}' " \
        f"font-family='{font_styles[0]}' fill='{font_styles[1]}' " \
        f"font-size='{font_styles[2]}'>{string}</text>"


utils.print_params(DEFAULT)

svg_list = []
# fill svg_list with svg objects
for text_obj in range(OBJECT_COUNT):
    text_str = random_text_string(random.randint(1, 10),
                                  [LOWER_CASE, UPPER_CASE, NUMBERS])
    str_xy = svg.get_random_point(DEFAULT['DRAWABLE_AREA'])
    str_font_size = random.randint(*MIN_MAX_FONT_SIZE)
    # str_colour = svg.get_random_colour()
    styles = [FONT_FAMILY, FILL, str_font_size]
    svg_list.append(string_to_object(text_str, str_xy, styles))

doc = svg.build_svg_file(
    DEFAULT['PAPER_SIZE'], DEFAULT['DRAWABLE_AREA'], svg_list)
svg.write_file(DEFAULT['FILENAME'], doc)

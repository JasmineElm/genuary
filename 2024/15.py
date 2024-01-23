#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Genuary 2024 - Day 15: "Use a physics library."
    Well, I didn't do this, but created a tinkerbell plot instead
"""

import toml


# local libraries
from helpers import svg, utils, draw


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
A = 0.9
B = -0.6013
C = 2.0
D = 0.5
X = 0.01
Y = 0.01
N = 10000


# LOCAL FUNCTIONS


def tinkerbell_attractor(a, b, c, d, x, y, n):
    """
    Generates a sequence of coordinates for the Tinkerbell map, which is a type of chaotic map.

    Parameters:
    a, b, c, d (float): The parameters of the Tinkerbell map.
    x, y (float): The initial coordinates.
    n (int): The number of iterations to perform.

    Returns:
    list: A list of tuples representing the coordinates at each iteration.
    """
    coordinates = []
    for _ in range(n):
        x, y = x*x - y*y + a*x + b*y, 2*x*y + c*x + d*y
        # print(x, y)
        coordinates.append((x, y))
    return coordinates


def map_range(value, low1, high1, low2, high2):
    """
    Maps a given value from one range to another.

    Parameters:
    value (float): The value to be re-mapped.
    low1, high1 (float): The bounds of the value's current range.
    low2, high2 (float): The bounds of the value's target range.

    Returns:
    float: The re-mapped value, which will be within the target range.
    """
    return low2 + (high2 - low2) * (value - low1) / (high1 - low1)


def get_dimensions(drawable_area):
    """
    Calculates the width and height of a drawable area.

    Parameters:
    drawable_area (tuple): A tuple of four elements representing the
    coordinates of the top left and bottom right corners of the drawable area.
    The elements are in the order (x1, y1, x2, y2), where (x1, y1) are the
    coordinates of the top left corner and (x2, y2) are the coordinates of the
    bottom right corner.

    Returns:
    tuple: A tuple of two elements representing the width and height of the
           drawable area.
    """
    return drawable_area[2] - drawable_area[0], \
        drawable_area[3] - drawable_area[1]


def draw_point(x, y, r):
    """ like a circle, but without styles..."""
    return f"<circle cx='{x}' cy='{y}' r='{r}' />"


# range goes from (-1 - 1) to (1,  1) map that to CEntre of the page
CENTRE = svg.get_centre(DEFAULT['DRAWABLE_AREA'])
canvas_min_x, canvas_min_y, canvas_max_x, canvas_max_y = DEFAULT['DRAWABLE_AREA']

svg_list = []
circle_list = []
circle_list.append(tinkerbell_attractor(A, B, C, D, X, Y, N))
# add the circles to the canvas


# work out min and max x, and y values
list_min_x = min(circle_list[0], key=lambda t: t[0])[0]
list_max_x = max(circle_list[0], key=lambda t: t[0])[0]
list_min_y = min(circle_list[0], key=lambda t: t[1])[1]
list_max_y = max(circle_list[0], key=lambda t: t[1])[1]

for circle in circle_list:
    for x_pos, y_pos in circle:
        x_pos = map_range(x_pos, list_min_x, list_max_x,
                          canvas_min_x, canvas_max_x)
        y_pos = map_range(y_pos, list_min_y, list_max_y,
                          canvas_min_y, canvas_max_y)
        svg_list.append(draw.circle((x_pos, x_pos), 1,
                                    ("black", 0, "black")))


utils.print_params(DEFAULT)


doc = svg.build_svg_file(
    DEFAULT['PAPER_SIZE'], DEFAULT['DRAWABLE_AREA'], svg_list)
# print(utils.calc_output_size(doc))
svg.write_file(DEFAULT['FILENAME'], doc)

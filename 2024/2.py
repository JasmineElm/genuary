#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Genuary 2024, prompt 2: "No palettes."
"""
import toml

# local libraries
from helpers import svg, utils, draw
import random

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

NOISE = 0.05
CIRCLE_COUNT = 30

# LOCAL FUNCTIONS


def get_random_colour():
    """Return a random hex colour string."""
    hex_colour = "#"+hex(random.randint(0, 16777215))[2:]
    return hex_colour


def skew_centre(viewport):
    """Returns a tuple with the coordinates of the centre of the canvas,
    skewed by a random amount.

    Args:
      viewport [list]: list of min_x, min_y, max_x, max_y

    Returns:
      tuple: A tuple with the x and y coordinates of the skewed centre of the
      canvas.
    """
    skewed_x = viewport[0] + \
        (viewport[2] - viewport[0]) * \
        (1+utils.weighted_random(NOISE)) / 2
    skewed_y = viewport[1] + \
        (viewport[3] - viewport[1]) * \
        (1+utils.weighted_random(NOISE)) / 2
    return ([int(skewed_x), int(skewed_y)])


def generate_circle_list(viewport, circle_count):
    """
    Generate a list of circle radii.

    Args:
      paper_size (tuple): The size of the paper to draw on.
      circle_count (int): The number of circles to generate.

    Returns:
      list: A list of circle radii.

    """
    max_radius = svg.calculate_max_radius(viewport) * 0.95
    circle_list = []
    for i in range(circle_count):
        circle = int(max_radius * ((i+i*utils.weighted_random(NOISE))
                                   / circle_count))
        if circle < max_radius:
            circle_list.append(circle)
        else:
            circle_list.append(max_radius)
    # reverse the list
    circle_list.reverse()
    return circle_list


def draw_circle(xy_pos, radius, style_list, opacity):
    """
    Returns an SVG circle element as a string with the specified center
    coordinates and radius.

    Args:
        cx (float): The x-coordinate of the center of the circle.
        cy (float): The y-coordinate of the center of the circle.
        r (float): The radius of the circle.

    Returns:
        str: An SVG circle element as a string.
    """
    circle_def = f"<circle cx='{xy_pos[0]}' cy='{xy_pos[1]}' r='{radius}' "
    circle_style = f"stroke='{style_list[0]}' stroke-width='{style_list[1]}' "
    circle_style += f"fill='{style_list[2]}'"
    circle_style += f" opacity='{opacity}'/>"
    return circle_def + "\n" + circle_style + "\n"


svg_list = []
# fill svg_list with svg objects
for circle_def in generate_circle_list(DEFAULT["DRAWABLE_AREA"], CIRCLE_COUNT):
    skew_xy = skew_centre(DEFAULT["DRAWABLE_AREA"])
    svg_list.append(draw_circle(skew_xy,
                                circle_def,
                                (255, 0, get_random_colour()),
                                random.random()))

doc = svg.build_svg_file(
    DEFAULT['PAPER_SIZE'], DEFAULT['DRAWABLE_AREA'], svg_list)
svg.write_file(DEFAULT['FILENAME'], doc)

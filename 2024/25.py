#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    genuary 2024 day 25: “I should try to recreate this with code”
"""
import random
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
WHITE_CIRCLE_STYLE = {'fill': '#fff', 'stroke': 'none'}
BLACK_CIRCLE_STYLE = {'fill': '#000', 'stroke': 'none'}
MAX_RADIUS = 1500
MIN_RADIUS = 150
CIRCLES_PER_MIN_RADIUS = 3
REPEAT = 50
# LOCAL FUNCTIONS


def set_radius(min_radius, max_radius, min_circles):
    """return a random radius between min_radius and max_radius, divisible by
    min_radius
    also return the number of circles that can fit in the radius"""
    # choose a random radius of step size min_radius
    step_size = max_radius // min_radius
    rad = random.randint(1, step_size) * min_radius
    # calculate the number of circles that can fit in the radius
    count = max(rad // min_radius, min_circles)
    return rad, count


def set_concentric_circles(centre, radius, circle_count):
    """Returns a list of concentric circles.

    Args:
      centre (tuple): x and y coordinates of the centre of the circles.
      radius (int): radius of the largest circle.
      circle_count (int): number of circles to draw.

    Returns:
      list: A list of circles.
    """
    circles = []
    step_size = radius // circle_count
    bcs = svg.dict_to_tags(BLACK_CIRCLE_STYLE)
    wcs = svg.dict_to_tags(WHITE_CIRCLE_STYLE)
    for i in range(circle_count):
        circle_size = radius - (step_size*i)
        if i % 2 == 0:
            circles.append(draw.circle2(centre, circle_size, bcs))
        else:
            circles.append(draw.circle2(centre, circle_size, wcs))
    return circles


utils.print_params(DEFAULT)

svg_list = []
# fill svg_list with svg objects
# set background and clippingpath
svg_list.append(svg.set_background(DEFAULT['DRAWABLE_AREA'], "#fff"))
svg_list.append(svg.set_clip_path(DEFAULT['DRAWABLE_AREA']))
# draw_centre = svg.get_centre(DEFAULT['DRAWABLE_AREA'])
for _ in range(REPEAT):
    draw_centre = svg.get_random_point(DEFAULT['DRAWABLE_AREA'])
    draw_radius, draw_circle_count = set_radius(
        MIN_RADIUS, MAX_RADIUS, CIRCLES_PER_MIN_RADIUS)
    print(f"radius: {draw_radius}, circle_count: {draw_circle_count}")
    circles_list = set_concentric_circles(
        draw_centre, draw_radius, draw_circle_count)
    for circle in circles_list:
        svg_list.append(circle)

doc = svg.build_svg_file(
    DEFAULT['PAPER_SIZE'], DEFAULT['DRAWABLE_AREA'], svg_list)
svg.write_file(DEFAULT['FILENAME'], doc)

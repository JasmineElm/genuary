#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Genuary 2024 - Day 19: "Flocking"
    remix  of day 16: Draw 10,000 of something
"""
import random
import math
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
LINE_LEN = 50
LINE_COUNT = 20000


STYLES = {"stroke": "#000",
          "stroke-width": "5",
          "clip-path": "url(#clip)"}


def draw_line_group(xy_list, addnl_styles):
    """return path from xy to dist_xy"""
    styles = svg.dict_to_tags(addnl_styles)
    path_parts = [f"M{point[0]} {point[1]} l{point[2]} {point[3]}"
                  for point in xy_list]
    path = f"<path d='{path_parts[0]} " \
        + " ".join(path_parts[1:]) + f"' {styles} />"
    return path


def set_path(start_xy, rotation, length, absolute=True, max_rot=180):
    """
    Generates an SVG path string for a line.

    Parameters:
    start_xy (list): A list of two elements representing the x and y
                     coordinates of the start point of the line.
    rotation (float): The rotation angle of the line in degrees.
    length (float): The length of the line.
    addnl_styles (dict): A dictionary of SVG styles to apply to the line.
    absolute (bool): Whether to return a positive rotation angle.
    max_rot (float): The maximum rotation angle.

    Returns:
    str: An SVG path string that defines a line with the given styles.
    """
    if absolute:
        rotation = abs(rotation) % max_rot
    else:
        rotation = rotation % max_rot
    start_xy = [int(start_xy[0]), int(start_xy[1])]
    end_xy = [start_xy[0] + length * math.cos(math.radians(rotation)),
              start_xy[1] + length * math.sin(math.radians(rotation))]
    dist_xy = [int(end_xy[0] - start_xy[0]), int(end_xy[1] - start_xy[1])]
    return (start_xy[0], start_xy[1], dist_xy[0], dist_xy[1])


def set_background(viewbox, colour):
    """set a path rectangle of colour the size of the viewbox"""
    return f"<path id='background' d='M{viewbox[0]} {viewbox[1]} " \
        + f"L{viewbox[2]} {viewbox[1]} L{viewbox[2]} {viewbox[3]} " \
        + f"L{viewbox[0]} {viewbox[3]} L{viewbox[0]} {viewbox[1]}' " \
        + f"fill='{colour}' />"


def set_clip_path(viewbox):
    """set a path rectangle of colour the size of the viewbox"""
    return "<defs><clipPath id='clip'><path id='background' " \
        + f"d='M{viewbox[0]} {viewbox[1]} " \
        + f"L{viewbox[2]} {viewbox[1]} L{viewbox[2]} {viewbox[3]} " \
        + f"L{viewbox[0]} {viewbox[3]} L{viewbox[0]} {viewbox[1]}' " \
        + "fill='none' /></clipPath></defs>"


def get_random_point_on_canvas(viewbox):
    """random point on canvas

    Args:
        viewbox (list): list of min_x, min_y, max_x, max_y

    Returns:
        list: list of [x, y] coordinates
    """
    x_pos = random.randint(viewbox[0], viewbox[2])
    y_pos = random.randint(viewbox[1], viewbox[3])
    return [x_pos, y_pos]


def calculate_rotation(init_xy, dest_xy):
    """calculate the angle between two points"""
    dx = dest_xy[0] - init_xy[0]
    dy = dest_xy[1] - init_xy[1]
    rot = math.degrees(math.atan2(dy, dx))
    return rot


utils.print_params(DEFAULT)

CENTRE = get_random_point_on_canvas(DEFAULT['DRAWABLE_AREA'])

svg_list = []
# fill svg_list with svg objects
# set background and clippingpath
svg_list.append(set_background(DEFAULT['DRAWABLE_AREA'], "#fff"))
svg_list.append(set_clip_path(DEFAULT['DRAWABLE_AREA']))
coords = []
for i in range(LINE_COUNT):
    start_pos = get_random_point_on_canvas(DEFAULT['DRAWABLE_AREA'])
    angle = calculate_rotation(start_pos, CENTRE)
    coords.append(set_path(start_pos, angle, LINE_LEN))
svg_list.append(draw_line_group(coords, STYLES))

doc = svg.build_svg_file(
    DEFAULT['PAPER_SIZE'], DEFAULT['DRAWABLE_AREA'], svg_list)
# strip all newlines and tabs

svg.write_file(DEFAULT['FILENAME'], doc, mini=True)

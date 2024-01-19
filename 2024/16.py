#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Genuary 2024 - Day 16: Draw 10,000 of something
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
    DEFAULT['OUTPUT_DIR']) + "16.svg"})


# LOCAL VARIABLES
MIN_X, MIN_Y, MAX_X, MAX_Y = DEFAULT['DRAWABLE_AREA']
LINE_LEN = 40
# ROWS = 7000
GAP = 3

DRAWABLE_AREA_WIDTH = MAX_X - MIN_X
DRAWABLE_AREA_HEIGHT = MAX_Y - MIN_Y
print(f"DRAWABLE_AREA_WIDTH: {DRAWABLE_AREA_WIDTH}")
print(f"DRAWABLE_AREA_HEIGHT: {DRAWABLE_AREA_HEIGHT}")
ROWS = DRAWABLE_AREA_WIDTH // LINE_LEN + GAP
ROW_WIDTH = DRAWABLE_AREA_WIDTH // LINE_LEN + GAP
ROW_HEIGHT = DRAWABLE_AREA_HEIGHT // ROWS
print(f"ROWS: {ROWS}")
print(f"ROW_WIDTH: {ROW_WIDTH}")
print(f"ROW_HEIGHT: {ROW_HEIGHT}")
STYLES = {"stroke": "#444", "stroke-width": "3"}


def draw_line_group(xy_list, addnl_styles):
    """return path from xy to dist_xy"""
    styles = svg.dict_to_tags(addnl_styles)
    path_parts = [f"M{point[0]} {point[1]} l{point[2]} {point[3]}"
                  for point in xy_list]
    path = f"<path d='{path_parts[0]} " \
        + " ".join(path_parts[1:]) + f"' {styles} />"
    return path


def set_path(start_xy, rotation, length):
    """
    Generates an SVG path string for a line.

    Parameters:
    start_xy (list): A list of two elements representing the x and y
                     coordinates of the start point of the line.
    rotation (float): The rotation angle of the line in degrees.
    length (float): The length of the line.
    addnl_styles (dict): A dictionary of SVG styles to apply to the line.

    Returns:
    str: An SVG path string that defines a line with the given styles.
    """
    rotation = abs(rotation) % 180
    start_xy = [int(start_xy[0]), int(start_xy[1])]
    end_xy = [start_xy[0] + length * math.cos(math.radians(rotation)),
              start_xy[1] + length * math.sin(math.radians(rotation))]
    dist_xy = [int(end_xy[0] - xy[0]), int(end_xy[1] - xy[1])]
    return (start_xy[0], start_xy[1], dist_xy[0], dist_xy[1])


utils.print_params(DEFAULT)

svg_list = []
# set a grid of LINE_LEN x LINE_LEN
y = MIN_Y + ROW_HEIGHT
cnt = 0
path_list = []
MAX_ROT = random.randint(0, 180)  # > 90 will "cycle" the line
# MAX_ROT = 45
for rows in range(ROWS):
    y += ROW_HEIGHT + GAP
    rot = random.randint(0, MAX_ROT)  # random start rotation
    # rot = 0  # always start at 0
    # set rot outside this loop to cycle over multiple lines
    MAX_ROT = random.randint(0, 90)  # > 90 will "cycle" the line
    for cols in range(ROW_WIDTH):
        # set the x and y coordinates of the centre of the circle
        x = MIN_X + (LINE_LEN * cols) + (LINE_LEN // 2)
        xy = [x, y]
        rot += MAX_ROT/ROW_WIDTH
        pth = set_path(xy, rot, LINE_LEN)
        path_list.append(pth)
        cnt += 1
        print(f"cnt: {cnt}")
    svg_list.append(draw_line_group(path_list, STYLES))
    path_list = []

doc = svg.build_svg_file(
    DEFAULT['PAPER_SIZE'], DEFAULT['DRAWABLE_AREA'], svg_list)
# strip all newlines and tabs

svg.write_file(DEFAULT['FILENAME'], doc, mini=True)

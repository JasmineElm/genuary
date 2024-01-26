#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Genuary 2024 - Day 15: "Use a physics library."
    Possibly PyMunk?
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
    DEFAULT['OUTPUT_DIR']) + "14.svg"})


# LOCAL VARIABLES
MIN_X, MIN_Y, MAX_X, MAX_Y = DEFAULT['DRAWABLE_AREA']
ROWS = 7
GAP = 25
MIN_RECT_PER_ROW = 2
MAX_RECT_PER_ROW = 6
DRAWABLE_AREA_WIDTH = MAX_X - MIN_X
DRAWABLE_AREA_HEIGHT = MAX_Y - MIN_Y
print(f"DRAWABLE_AREA_WIDTH: {DRAWABLE_AREA_WIDTH}")
print(f"DRAWABLE_AREA_HEIGHT: {DRAWABLE_AREA_HEIGHT}")
MIN_WIDTH = DRAWABLE_AREA_WIDTH // MAX_RECT_PER_ROW + GAP
MAX_WIDTH = DRAWABLE_AREA_WIDTH // MIN_RECT_PER_ROW + GAP
ROW_HEIGHT = DRAWABLE_AREA_HEIGHT // ROWS
STYLES = {"fill": "#444"}
print(f"MIN_WIDTH: {MIN_WIDTH}")
print(f"MAX_WIDTH: {MAX_WIDTH}")

# LOCAL FUNCTIONS


def threecharhex():
    """ return a random 3 character hex colour """
    return f"#{random.randint(0, 0xfff):03x}"


def mini_grid(rect_def_list, styles):
    """ set a grid of rectangles"""
    head = "<path d=\""
    tail = f"\" {svg.dict_to_tags(styles)}/>"
    body = ""
    for rect in rect_def_list:
        body += f"M{rect[0]} {rect[1]}h{rect[2]}v{rect[3]}H{rect[0]}z"
    return head + body + tail


utils.print_params(DEFAULT)

svg_list = []
# draw a grid of rectangles, rows high
start_xy = [DEFAULT['DRAWABLE_AREA'][0], DEFAULT['DRAWABLE_AREA'][1]]
# add a gap between each row
for i in range(ROWS):
    # each row separated by GAP
    row_y = start_xy[1] + i * (ROW_HEIGHT + GAP)
    row_x = start_xy[0]
    rect_defs = []
    while row_x < MAX_X:
        # each row has a random number of rectangles
        print(f"row_x: {row_x}")  # DEBUG
        width = random.randint(MIN_WIDTH, MAX_WIDTH)
        # if width+gap>max_x, then width = max_x - gap
        if row_x + width + GAP > MAX_X:
            width = MAX_X - row_x - GAP
        rect_defs.append([row_x, row_y, width, ROW_HEIGHT])
        row_x += width + GAP
    STYLES.update({"fill": threecharhex()})
    svg_list.extend([mini_grid(rect_defs, STYLES)])


doc = svg.build_svg_file(
    DEFAULT['PAPER_SIZE'], DEFAULT['DRAWABLE_AREA'], svg_list)
# strip all newlines and tabs

svg.write_file(DEFAULT['FILENAME'], doc, mini=True)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Genuary 2024 - Day 23: "64*64"
"""
import toml
import numpy as np
import random

# local libraries
from helpers import svg, utils, draw

# Load config file and set DEFAULT parameters
config = toml.load("config.toml")
DEFAULT = config["DEFAULT"]
PAPER_SIZE = config["paper_sizes"]["C64"]
PPMM = 1
print(PAPER_SIZE)
DEFAULT.update({"PAPER_SIZE": svg.set_image_size(PAPER_SIZE,
                                                 PPMM,
                                                 DEFAULT['LANDSCAPE'])})
DEFAULT.update({"DRAWABLE_AREA": svg.set_drawable_area(DEFAULT['PAPER_SIZE'],
                                                       DEFAULT['BLEED'])})
DEFAULT.update({"FILENAME": utils.create_dir(
    DEFAULT['OUTPUT_DIR']) + utils.generate_filename()})


# LOCAL VARIABLES
STYLES = {"stroke": "black", "stroke-width": 4, "fill": "none", "stroke-linecap": "round"}

# LOCAL FUNCTIONS


def draw_box(xy, size, addnl_styles):
    """draw a box with the specified style"""
    # use dict_to_tags to convert the dict to a string of svg tags
    styles = svg.dict_to_tags(addnl_styles)
    box = f"<path d='M {xy[0]} {xy[1]} "
    box += f"h {size} v {size} h -{size} z' {styles} />"
    return box


svg_list = []
# find largest square that fits in drawable area that's divisible by 64
# use that as the grid size
min_dim = min(DEFAULT['DRAWABLE_AREA'][2]-DEFAULT['DRAWABLE_AREA'][0],
              DEFAULT['DRAWABLE_AREA'][3]-DEFAULT['DRAWABLE_AREA'][1])

# print(min_dim)
# work out largest multiple of 64 that fits in min_dim
grid_size = 64 * int(min_dim / 64)
pad = min_dim - grid_size / 2
centre = svg.get_centre(DEFAULT['DRAWABLE_AREA'])




utils.print_params(DEFAULT)

# draw a grid of 64x64 squares
for x in np.arange(centre[0]-grid_size/2, centre[0]+grid_size/2, 64):
    for y in np.arange(centre[1]-grid_size/2, centre[1]+grid_size/2, 64):
        rand_val = random.random()
        if rand_val < 0.4:
            svg_list.append(draw.line([x, y], [x+64, y+64], STYLES))
        elif rand_val < 0.8:
            svg_list.append(draw.line([x, y+64], [x+64, y], STYLES))
        else:
            svg_list.append(draw_box([x, y], 64, STYLES))

doc = svg.build_svg_file(
    DEFAULT['PAPER_SIZE'], DEFAULT['DRAWABLE_AREA'], svg_list)
svg.write_file(DEFAULT['FILENAME'], doc)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Genuary 2024 - Day 18: "Bauhaus"
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
LINE_STYLES = {"stroke": "#000",
               "stroke-width": "10",
               "fill": "none",
               "clip-path": "url(#clip)"}
GAP = 30
MIN_XY = DEFAULT['DRAWABLE_AREA'][0:2]

# LOCAL FUNCTIONS


def draw_box(rect_def_list, styles):
    """
    Generates an SVG path element representing a mini grid.

    Args:
        rect_def_list (list): x,y,w,h of square
        styles (dict): A dictionary of SVG styles.

    Returns:
        str: An SVG path element as a string.
    """
    rdf = rect_def_list
    head = "<path d=\""
    body = f"M{rdf[0]} {rdf[1]}h{rdf[2]}v{rdf[3]}H{rdf[0]}z"
    tail = f"\" {svg.dict_to_tags(styles)}/>"
    return head + body + tail


def set_max_square_size(drawable_area, gap):
    """ set a box size based on the drawable area and gap """
    min_x, min_y, max_x, max_y = drawable_area
    width = max_x - min_x
    height = max_y - min_y
    # square size is the smallest of the two
    square_size = min(width, height)
    return square_size - (gap*2)


utils.print_params(DEFAULT)

svg_list = []
# set backbround and clip path
svg_list.append(svg.set_background(DEFAULT['DRAWABLE_AREA'], "#fff"))
svg_list.append(svg.set_clip_path(DEFAULT['DRAWABLE_AREA']))


# Centre is anywhere between min_x and (max_x -min_x)//2 Y is anywhere between
# min_y and max_y
CENTRE = [random.randint(MIN_XY[0], (DEFAULT['DRAWABLE_AREA'][2] - MIN_XY[0])//3),
          random.randint(MIN_XY[1], DEFAULT['DRAWABLE_AREA'][3])]
# while min_x OR max_x are in canvas, draw a box, incrementing the size by gap
# each time
square_size = GAP
# while either Y, or Y+square_size are in drawable area
while (CENTRE[1] > MIN_XY[1]) or (CENTRE[1] + square_size < DEFAULT['DRAWABLE_AREA'][3]):
    square_size += (GAP*2)
    # increment CENTRE by GAP
    CENTRE[0] -= GAP
    CENTRE[1] -= GAP
    draw_rect_def_list = [CENTRE[0], CENTRE[1], square_size, square_size]
    svg_list.append(draw_box(draw_rect_def_list, LINE_STYLES))
    max_x = CENTRE[0] + square_size
CENTRE = [max_x, MIN_XY[1] - GAP]

square_size = set_max_square_size(DEFAULT['DRAWABLE_AREA'], GAP) * 2

while square_size > GAP*2:
    square_size -= (GAP*2)
    # increment CENTRE by GAP
    CENTRE[0] += GAP
    CENTRE[1] += GAP
    draw_rect_def_list = [CENTRE[0], CENTRE[1], square_size, square_size]
    svg_list.append(draw_box(draw_rect_def_list, LINE_STYLES))
    max_x = CENTRE[0] + square_size + GAP

doc = svg.build_svg_file(
    DEFAULT['PAPER_SIZE'], DEFAULT['DRAWABLE_AREA'], svg_list)
svg.write_file(DEFAULT['FILENAME'], doc)

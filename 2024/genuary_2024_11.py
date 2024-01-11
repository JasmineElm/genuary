#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Genuary 2024 - Day 11: "In the style of Anni Albers (1899-1994)."
    a riff on TR IIIA, 1969-70:
    https://www.tate.org.uk/art/artworks/albers-tr-iii-p14776
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
    DEFAULT['OUTPUT_DIR']) + "11.svg"})


# LOCAL VARIABLES
TRIANGLE_HEIGHT = 50
TRIANGLE_WIDTH = 100
UPNESS = 0.85
SPACEYNESS = 0.2
SPARSENESS = 0.1
BACKGROUND_COLOUR = "#76512d"
FOREGROUND_COLOUR = "#9b7046"
EXTRA_TAGS = {"stroke": "none", "stroke-width": "0", "fill": FOREGROUND_COLOUR}
TAGS = svg.dict_to_tags(EXTRA_TAGS)

HEIGHT = DEFAULT['DRAWABLE_AREA'][3] - DEFAULT['DRAWABLE_AREA'][1]
WIDTH = DEFAULT['DRAWABLE_AREA'][2] - DEFAULT['DRAWABLE_AREA'][0]

ROWS = HEIGHT // TRIANGLE_HEIGHT
COLS = WIDTH // TRIANGLE_WIDTH

# modulo cols to find unused space

COL_SPACE = WIDTH % (COLS*TRIANGLE_WIDTH)
ROW_SPACE = HEIGHT % (ROWS*TRIANGLE_HEIGHT)

START_X = DEFAULT['DRAWABLE_AREA'][0]
START_Y = DEFAULT['DRAWABLE_AREA'][1]


# LOCAL FUNCTIONS


def draw_triangle(xy_pos, point_pos, extra_tags):
    """draw a triangle"""
    # point_pos is list of 3 tuples
    # each tuple is an xy position relative to xy
    # extra_tags is a dict of extra tags to add to the svg element
    triangle = f"<polygon points='{xy_pos[0]+ point_pos[0][0]} {xy_pos[1]+ point_pos[0][1]} "
    triangle += f"{xy_pos[0]+ point_pos[1][0]} {xy_pos[1]+ point_pos[1][1]} "
    triangle += f"{xy_pos[0]+ point_pos[2][0]} {xy_pos[1]+ point_pos[2][1]}' "
    triangle += f"{extra_tags if extra_tags else ''} />"
    return triangle


def triangle_dir(up_down, width, height):
    """return a list of 3 tuples of xy positions for a triangle"""
    # up_down is a string, one of "up", "down", "left", "right"
    # width and height are the width and height of the triangle
    if up_down == "up":
        return [(0, height), (width, height), (width//2, 0)]
    if up_down == "down":
        return [(0, 0), (width, 0), (width//2, height)]


def rand_bool():
    """return a random boolean"""
    return random.choice([True, False])


# utils.print_params(DEFAULT)
svg_list = []
# fill svg_list with svg objects
background = draw.set_background(DEFAULT['DRAWABLE_AREA'],
                                 BACKGROUND_COLOUR)
svg_list.append(background)
xy = [START_X, START_Y+TRIANGLE_HEIGHT//2]
for row in range(ROWS-2):
    xy[0] = START_X
    xy[1] += TRIANGLE_HEIGHT
    while xy[0] < DEFAULT['DRAWABLE_AREA'][2] - TRIANGLE_WIDTH:
        spcr = TRIANGLE_WIDTH // 2 if random.random() < SPACEYNESS else 0
        xy[0] += spcr
        DIRECTION = "up" if random.random() < UPNESS else "down"
        point_pos = triangle_dir(DIRECTION, TRIANGLE_WIDTH, TRIANGLE_HEIGHT)
        if random.random() > SPARSENESS:
            svg_list.append(draw_triangle(xy, point_pos, TAGS))
        xy[0] += TRIANGLE_WIDTH
doc = svg.build_svg_file(
    DEFAULT['PAPER_SIZE'], DEFAULT['DRAWABLE_AREA'], svg_list)
svg.write_file(DEFAULT['FILENAME'], doc)

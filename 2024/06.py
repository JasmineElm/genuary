#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    genuary 2024, day 6: "Screensaver."
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

SEGMENT_LENGTH = 60
OVERALL_LENGTH = 255
STROKE_COLOUR = '#000000'
STROKE_WIDTH = 30
FILL_COLOUR = 'none'
STYLES = (STROKE_COLOUR, STROKE_WIDTH, FILL_COLOUR)


# LOCAL FUNCTIONS


def draw_path(xy, canvas, segment_length):
    init_xy = xy
    x, y = xy
    coords = []
    while xy != init_xy or len(coords) == 0:
        x, y = xy
        coords.append((x, y))
        on_canvas = True
        while on_canvas:
            direction = random.choice([0, 90, 270])
            # if x < canvas[0], set x to canvas[2]
            if direction == 0:
                x += segment_length
            elif direction == 90:
                y += segment_length
            elif direction == 180:
                x -= segment_length
            elif direction == 270:
                y -= segment_length
            coords.append((x, y))
            if (x < canvas[0] or x > canvas[2]
                or y < canvas[1] or y > canvas[3]): # noqa E129
                on_canvas = False
    return coords


utils.print_params(DEFAULT)

svg_list = []
# fill svg_list with svg objects
start_pos = svg.get_random_coordinates(DEFAULT['DRAWABLE_AREA'])
start_pos = svg.get_centre(DEFAULT['DRAWABLE_AREA'])
colour = STYLES[0]
for i in range(OVERALL_LENGTH):
    coordinates = draw_path(start_pos, DEFAULT['DRAWABLE_AREA'],
                            SEGMENT_LENGTH)
    start_pos = coordinates[-1]
    if start_pos[0] < DEFAULT['DRAWABLE_AREA'][0]:
        start_pos = (DEFAULT['DRAWABLE_AREA'][2], start_pos[1])
    elif start_pos[0] > DEFAULT['DRAWABLE_AREA'][2]:
        start_pos = (DEFAULT['DRAWABLE_AREA'][0], start_pos[1])
    elif start_pos[1] < DEFAULT['DRAWABLE_AREA'][1]:
        start_pos = (start_pos[0], DEFAULT['DRAWABLE_AREA'][3])
    elif start_pos[1] > DEFAULT['DRAWABLE_AREA'][3]:
        start_pos = (start_pos[0], DEFAULT['DRAWABLE_AREA'][1])
    # increment colour
    colour = svg.get_random_colour()
    path = draw.path(coordinates, (colour, STYLES[1], STYLES[2]))
    svg_list.append(path)

doc = svg.build_svg_file(
    DEFAULT['PAPER_SIZE'], DEFAULT['DRAWABLE_AREA'], svg_list)
svg.write_file(DEFAULT['FILENAME'], doc)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Genuary 2024, prompt 3: "Droste Effect."
    Couldn't see how to do this, so have gone with a simple recursive tiling
    pattern.
"""
import random
import toml
# local libraries
from helpers import svg, utils, draw


# Load config file and set DEFAULT parameters
config = toml.load("config.toml")
DEFAULT = config["DEFAULT"]
DEFAULT.update(
    {
        "PAPER_SIZE": svg.set_image_size(
            DEFAULT["SIZE"], DEFAULT["PPMM"], DEFAULT["LANDSCAPE"]
        )
    }
)
DEFAULT.update(
    {"DRAWABLE_AREA": svg.set_drawable_area(DEFAULT["PAPER_SIZE"],
                                            DEFAULT["BLEED"])}
)
DEFAULT.update(
    {"FILENAME": utils.create_dir(
        DEFAULT["OUTPUT_DIR"]) + utils.generate_filename()}
)


# LOCAL VARIABLES
RECURSION = 9
LINE_WIDTH = 5
COLOUR = "#000000"
# LOCAL FUNCTIONS


def split_space(space, direction):
    """halve a space in a given direction

    Args:
        space (tuple): [min_x, min_y, max_x, max_y]
        direction (int): 0 = horizontal, 1 = vertical

    Returns:
        space (tuple): [min_x, min_y, max_x, max_y]
    """
    if direction == 0:
        # split horizontally
        split = [space[0], space[1], space[2], space[3]//2]
    if direction == 1:
        # split vertically
        split = [space[0], space[1], space[2]//2, space[3]]
    return split


def is_rectangle_in_canvas(xy, size_x, size_y, canvas):
    """test if a rectangle is within the canvas"""
    if xy[0] + size_x < canvas[2] and xy[1] + size_y < canvas[3]:
        return [xy, size_x, size_y]
    else:
        return False


def tile(canvas, depth, line_width, colour):
    """
    Recursively divides a canvas into smaller rectangles and draws them.

    Args:
        canvas (list): A list of four int min_x, min_y, max_x, max_y.
        depth (int): The depth of recursion.
        line_width (int): The width of the lines to draw.
        colour (str): The colour of the lines to draw.

    Returns:
        list: A list of drawn rectangles.
    """
    # function body...
    if depth <= 0:
        return []
    full_canvas = canvas
    lines = []
    directions = [random.randint(0, 1) for _ in range(depth)]
    for direction in directions:
        split = split_space(canvas, direction)
        rectangles = [
            [split[0], split[1]],
            [canvas[2] - split[0], canvas[1]],
            [split[0], canvas[3] - split[1]],
            [canvas[2] - split[0], canvas[3] - split[1]]
        ]
        for xy in rectangles:
            size_x = split[2] - split[0]
            size_y = split[3] - split[1]
            if is_rectangle_in_canvas(xy, size_x, size_y, full_canvas):
                lines.append(draw.rectangle(xy,
                                            size_x,
                                            size_y,
                                            styles=(colour,
                                                    line_width,
                                                    'none')))
        canvas = split
        lines.extend(tile(canvas, depth-1, line_width, colour))
    # strip duplicates
    lines = list(set(lines))
    return lines


utils.print_params(DEFAULT)
svg_list = []
svg_list.append(svg.set_background(DEFAULT['DRAWABLE_AREA'], "#fff"))
svg_list.append(svg.set_clip_path(DEFAULT['DRAWABLE_AREA']))
draw_canvas = DEFAULT["DRAWABLE_AREA"]
# add a 5px bleed to the canvas
draw_canvas = [draw_canvas[0] + 5,
               draw_canvas[1] + 5,
               draw_canvas[2] - 5,
               draw_canvas[3] - 5]
for obj in tile(DEFAULT["DRAWABLE_AREA"], RECURSION, LINE_WIDTH, COLOUR):
    svg_list.append(obj)
    # strip duplicates
doc = svg.build_svg_file(DEFAULT["PAPER_SIZE"],
                         DEFAULT["DRAWABLE_AREA"], svg_list)
svg.write_file(DEFAULT["FILENAME"], doc)

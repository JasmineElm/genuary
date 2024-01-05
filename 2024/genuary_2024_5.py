#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    genuary 2024, proompt 5: "In the style of Vera Molnár (1924-2023)."
    attempt to recreate 16 Points 4 Gris (2ème vers) 1952-2007 (see link below)
    https://www.artnet.com/artists/vera-molnar/16-points-4-gris-2%C3%A8me-vers-1952-2007-A21ZCoqg5F5oDqZcBrc7og2
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
    {"DRAWABLE_AREA":
        svg.set_drawable_area(DEFAULT["PAPER_SIZE"], DEFAULT["BLEED"])}
)
DEFAULT.update(
    {"FILENAME":
        utils.create_dir(DEFAULT["OUTPUT_DIR"]) + utils.generate_filename()}
)


# LOCAL VARIABLES

GRID_SHAPE = [4, 4]  # number of objects in each direction
BLEED = 100  # pixel bleed around the edge of the canvas, between objects
HALF_BLEED = BLEED / 2
LIGHT_GREY = "#f0f0f0"
# LOCAL FUNCTIONS


def calculate_grid_size(canvas, bleed):
    """set grid_size to the minimum of the canvas width and height

    Args:
        canvas (tuple): [min_x, min_y, max_x, max_y]
        bleed (int): bleed around the edge of the canvas
    """
    local_grid_size = min(canvas[2] - canvas[0] - bleed,
                          canvas[3] - canvas[1] - bleed)
    return local_grid_size


def get_centre(canvas):
    """calculate the centre of the grid

    Args:
        canvas (tuple): [min_x, min_y, max_x, max_y]
        grid_size (int): size of the grid
    """
    centre_x = (canvas[2] - canvas[0]) / 2
    centre_y = (canvas[3] - canvas[1]) / 2
    return (centre_x, centre_y)


def set_segment(grid_size, bleed, grid_shape):
    """set the size of a segment

    Args:
        grid_size (int): size of the grid
        bleed (int): bleed around the edge of the canvas
        grid_shape (list): number of objects in each direction
    """
    segment_x = (grid_size - bleed) / grid_shape[0]
    segment_y = (grid_size - bleed) / grid_shape[1]
    return (segment_x, segment_y)


def set_largest_object(segment, bleed):
    """set the size of the largest object

    Args:
        segment (tuple): size of a segment
    """
    largest_object = min(segment[0], segment[1]) - (bleed / 2)
    return largest_object


utils.print_params(DEFAULT)

svg_list = []
# set the grid size
draw_grid_size = calculate_grid_size(DEFAULT["DRAWABLE_AREA"], BLEED)
# draw a rectangle around it
centre = get_centre(DEFAULT["DRAWABLE_AREA"])
start_xy = (
    centre[0] + DEFAULT["DRAWABLE_AREA"][0] - draw_grid_size / 2,
    centre[1] + DEFAULT["DRAWABLE_AREA"][0] - draw_grid_size / 2,
)

svg_list.append(
    draw.rectangle(start_xy,
                   draw_grid_size,
                   draw_grid_size,
                   styles=("none", 0, LIGHT_GREY))
)

# draw a grid of circles
draw_segment = set_segment(draw_grid_size, BLEED, GRID_SHAPE)
largest_draw_object = set_largest_object(draw_segment, BLEED)
for row in range(GRID_SHAPE[0]):
    for col in range(GRID_SHAPE[1]):
        # calculate the centre of the circle
        half_segment = [draw_segment[0] / 2, draw_segment[1] / 2]
        centre = (
            start_xy[0] + draw_segment[0] * row + half_segment[0] + HALF_BLEED,
            start_xy[1] + draw_segment[1] * col + half_segment[1] + HALF_BLEED,
        )
        # draw the circle
        size = random.randint(1, 8) / 8  # quantized to 8ths
        # fill is size cast to hex(RBG)
        FILL = "#" + "".join(str(hex(int(size * 128)))[2:].zfill(2)
                             for _ in range(3))
        svg_list.append(
            draw.circle(centre,
                        size * largest_draw_object / 2,
                        style_list=("none", 0, FILL))
        )

doc = svg.build_svg_file(DEFAULT["PAPER_SIZE"],
                         DEFAULT["DRAWABLE_AREA"],
                         svg_list)
svg.write_file(DEFAULT["FILENAME"], doc)

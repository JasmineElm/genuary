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
    {"DRAWABLE_AREA":
        svg.set_drawable_area(DEFAULT["PAPER_SIZE"], DEFAULT["BLEED"])}
)
DEFAULT.update(
    {"FILENAME":
        utils.create_dir(DEFAULT["OUTPUT_DIR"]) + utils.generate_filename()}
)


# LOCAL VARIABLES
PALETTE_SIZE = 5
PIXEL_SIZE = 20

# LOCAL FUNCTIONS


def set_palette(length):
    """for each band, add a hex value to the palette"""
    channels = [random.randint(0, 1) for _ in range(3)]
    while sum(channels) == 0 or sum(channels) == 3:
        channels = [random.randint(0, 1) for _ in range(3)]
    local_palette = [
        ["#" + "".join(str(hex(random.randint(0, 255) * channel))[2:].zfill(2)
                       for channel in channels)]
        for _ in range(length)
    ]
    return local_palette


def draw_pixel(xy, size, colour):
    """draw a pixel"""
    return draw.rectangle(xy, size, size, [colour, 0, colour])


def set_band(canvas, bands, pixel_size):
    """return band width and height

    Args:
        canvas (tuple): min x, min y, max x, max y
        bands (int): count of bands
        pixel_size (int): size of pixel

    Returns:
        tuple: ints of width and height
    """
    # return band width and height
    divisor = bands * pixel_size
    width, height = (canvas[2] - canvas[0]) // divisor, (
        canvas[3] - canvas[1]
    ) // divisor

    return [width, height]


utils.print_params(DEFAULT)
svg_list = []

band_size = set_band(DEFAULT["DRAWABLE_AREA"], PALETTE_SIZE, PIXEL_SIZE)
palette = set_palette(PALETTE_SIZE)

# fill drawable area with pixels
da = DEFAULT["DRAWABLE_AREA"]
rows = (da[3] - da[1]) // PIXEL_SIZE
cols = (da[2] - da[0]) // PIXEL_SIZE

for row in range(rows):
    for col in range(cols):
        # choose a colour from the palette
        pixel_colour = palette[random.randint(0, PALETTE_SIZE - 1)][0]
        # draw a pixel
        svg_list.append(
            draw_pixel(
                [
                    DEFAULT["DRAWABLE_AREA"][0] + (col * PIXEL_SIZE),
                    DEFAULT["DRAWABLE_AREA"][1] + (row * PIXEL_SIZE),
                ],
                PIXEL_SIZE,
                pixel_colour,
            )
        )

doc = svg.build_svg_file(DEFAULT["PAPER_SIZE"],
                         DEFAULT["DRAWABLE_AREA"],
                         svg_list)
svg.write_file(DEFAULT["FILENAME"], doc)

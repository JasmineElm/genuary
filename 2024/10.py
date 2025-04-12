#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Genuary 2024 - Day 10: "Hexagonal."
"""
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

HEX_SPACING = 20
MAX_RADIUS = int(svg.get_min_dimension(DEFAULT['DRAWABLE_AREA']))
CENTRE = svg.get_centre(DEFAULT['DRAWABLE_AREA'])
STYLES = ['black', 1, 'none']
HEX_POINTS = 6

# LOCAL FUNCTIONS


def set_clip(obj, svg_id):
    """wrap object with masking tag"""
    mp = f"<defs>\n\t<clipPath id=\"{svg_id}\">\
        \n\t\t{obj}</clipPath>\n</defs>\n"
    return mp


utils.print_params(DEFAULT)

svg_list = []
svg_list.append(svg.set_background(DEFAULT['DRAWABLE_AREA'], "#fff"))
# svg_list.append(svg.set_clip_path(DEFAULT['DRAWABLE_AREA']))
# fill svg_list with svg objects
# fill canvas with concentric hexagons

# set our clip path
CLIP_PATH = svg.set_polygon(CENTRE, MAX_RADIUS, HEX_POINTS)
CLIP_PATH = utils.list_to_string(CLIP_PATH)
CLIP_PATH = set_clip(draw.polygon(CLIP_PATH, STYLES), 'clip')
svg_list.append(CLIP_PATH)

for radius in range(HEX_POINTS, MAX_RADIUS, HEX_SPACING):
    HX = svg.set_polygon(CENTRE, radius, HEX_POINTS)
    HX = utils.list_to_string(HX)
    svg_list.append(draw.polygon(HX, STYLES))
    # also append a circle
    circle = draw.circle(CENTRE, radius//2, STYLES,
                         addnl='clip-path="url(#clip)"')
    svg_list.append(circle)
    # set a clip path for the largest hexagon
# set a clip path for the largest hexagon


doc = svg.build_svg_file(
    DEFAULT['PAPER_SIZE'], DEFAULT['DRAWABLE_AREA'], svg_list)
svg.write_file(DEFAULT['FILENAME'], doc)

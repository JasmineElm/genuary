#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Genuary 2024 - Day 27: "Code for an hour."
"""
import toml

# local libraries
from helpers import svg, utils, draw, lsys

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
AXIOM = "-YF"
RULES = {"X": "XFX-YF-YF+FX+FX-YF-YFFX+YF+FXFXYF-FX+YF+FXFX+YF-FXYF-YF-FX+FX+YFYF-",
         "Y": "+FXFX-YF-YF+FX+FXYF+FX-YFYF-FX-YF+FXYFYF-FX-YFFX+FX+YF-YF-FX+FX+YFY"}
N = 3
LINE_LENGTH = 40
ANGLE = 90
ANGLE_OFFSET = 90
CENTRE = svg.get_centre(DEFAULT['DRAWABLE_AREA'])
LINE_STYLE = {'stroke': '#fff', 'stroke-width': 10, "stroke-linecap": "round"}
CENTRE = DEFAULT['DRAWABLE_AREA'][2] - 10, DEFAULT['DRAWABLE_AREA'][3] - 10

utils.print_params(DEFAULT)

svg_list = []
# draw background
svg_list.append(svg.set_background(DEFAULT['DRAWABLE_AREA'], "#000"))
svg_list.append(svg.set_background(
    DEFAULT['DRAWABLE_AREA'], "url(#gradient)"))
svg_list.append(svg.set_clip_path(DEFAULT['DRAWABLE_AREA']))

# fill svg_list with svg objects


LSYS_DEF = lsys.set_lsys_string(AXIOM, RULES, N)
line_defs = lsys.lsys_to_lines(
    LSYS_DEF, CENTRE, ANGLE, LINE_LENGTH, ANGLE_OFFSET)
for line in line_defs:
    # if all coords are in drawable area
    if svg.is_in_drawable_area(line[0], line[1], DEFAULT['DRAWABLE_AREA']):
        svg_list.append(draw.line(line[0], line[1], LINE_STYLE))
doc = svg.build_svg_file(
    DEFAULT['PAPER_SIZE'], DEFAULT['DRAWABLE_AREA'], svg_list)
svg.write_file(DEFAULT['FILENAME'], doc)

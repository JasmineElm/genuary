#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Genuary 2024 - Day 17: "Inspired by Islamic Art."
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
AXIOM = "F++F++F++F++F"
RULES = {"F": "F++F++F+++++F-F++F"}
N = 6
LINE_LENGTH = 250
ANGLE = 36
ANGLE_OFFSET = 36
CENTRE = svg.get_centre(DEFAULT['DRAWABLE_AREA'])
LINE_STYLE = {'stroke': '#fff', 'stroke-width': 15, "stroke-linecap": "round"}
CENTRE = svg.get_centre(DEFAULT['DRAWABLE_AREA'])
CENTRE = (CENTRE[0], DEFAULT['DRAWABLE_AREA'][3] + 1700)

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

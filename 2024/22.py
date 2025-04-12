#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Skeleton file for new scripts
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

rot_x = 0
rot_y = 0
rot = 0
scale = 1
TAGS = {"fill": "#000", "transform": f"rotate({rot}) skewX({rot_x}) skewY({rot_y}) scale({scale})"}
# LOCAL FUNCTIONS


utils.print_params(DEFAULT)

svg_list = []
svg_list.append(svg.set_background(DEFAULT['DRAWABLE_AREA'], "#fff"))
svg_list.append(svg.set_clip_path(DEFAULT['DRAWABLE_AREA']))
# fill svg_list with svg objects
CENTRE = svg.get_centre(DEFAULT['DRAWABLE_AREA'])
MAX_CIRCLE_RADIUS = svg.get_min_dimension(DEFAULT['DRAWABLE_AREA']) / 2

svg_list.append(draw.circle2(CENTRE, MAX_CIRCLE_RADIUS, TAGS))
for i in range(1, 10):
    # alter the transform dict to skewX and skewY +1 each time, rotate +1, and
    # scale -0.1
    # convert the transform dict to a string
    fill = svg.get_random_colour()
    rot_x += 1
    rot_y -= 1
    rot -= 1
    scale -= 0.1
    
    TAGS = {"fill": fill, "transform-origin": "center", "transform": f"rotate({rot}) skewX({rot_x}) skewY({rot_y}) scale({scale})"}
    svg_list.append(draw.box2(CENTRE, MAX_CIRCLE_RADIUS-i*10, TAGS))

doc = svg.build_svg_file(
    DEFAULT['PAPER_SIZE'], DEFAULT['DRAWABLE_AREA'], svg_list)
svg.write_file(DEFAULT['FILENAME'], doc)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Skeleton file for new scripts
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
FONT_STYLES = {"font-family": "sans-serif",
               "font-size": "500",
               "font-weight": "bold",
               "text-anchor": "middle",
               "fill": "#fff"}
WIDTH = DEFAULT['DRAWABLE_AREA'][2] - DEFAULT['DRAWABLE_AREA'][0]
HEIGHT = DEFAULT['DRAWABLE_AREA'][3] - DEFAULT['DRAWABLE_AREA'][1]
MIN_XY = DEFAULT['DRAWABLE_AREA'][:2]
# LOCAL FUNCTIONS


def svg_text(string, xy, font_styles):
    """ return svg text object"""
    font_styles = svg.dict_to_tags(font_styles)
    text = f"<text {font_styles} x='{xy[0]}' y='{xy[1]}'>{string}</text>"
    return text


def object_to_clip_path(obj, clip_id):
    """return path from xy to dist_xy"""
    clip_path = f"<defs><clipPath id='{clip_id}'>\n\t{obj}\n</clipPath></defs>"
    return clip_path


def set_background(viewbox, colour):
    """set a path rectangle of colour the size of the viewbox"""
    return f"<path id='background' d='M{viewbox[0]} {viewbox[1]} " \
        + f"L{viewbox[2]} {viewbox[1]} L{viewbox[2]} {viewbox[3]} " \
        + f"L{viewbox[0]} {viewbox[3]} L{viewbox[0]} {viewbox[1]}' " \
        + f"fill='{colour}' />"


def draw_circle(xy, radius, addnl_styles):
    """return a circle"""
    styles = svg.dict_to_tags(addnl_styles)
    return f"<circle cx='{xy[0]}' cy='{xy[1]}' r='{radius}' " \
        + f"{styles} />"


def random_colour(greyscale=False):
    # e.g., #ffffff
    if greyscale:
        colour = f"{random.randint(0, 255):02x}"
        colour = f"#{colour * 3}"
    else:
        colour = ''.join(f"{random.randint(0, 255):02x}" for _ in range(3))
        colour = f"#{colour}"
    return colour


def pixel_noise(xy, size, px_size, greyscale=False):
    """return a circle"""
    # size = xy[0] + size[0], xy[1] + size[1]
    for x in range(xy[0], size[0], px_size):
        for y in range(xy[1], size[1], px_size):
            colour = random_colour(greyscale)
            yield draw.box((x, y), px_size, (colour, 0, colour))


def objects_to_group(objects, group_id, addnl_styles):
    """return a group of objects"""
    styles = svg.dict_to_tags(addnl_styles)
    group = f"<g id='{group_id}' {styles}>\n"
    for obj in objects:
        group += f"\t{obj}\n"
    group += "</g>"
    return group


utils.print_params(DEFAULT)

svg_list = []
# fill svg_list with svg objects
CENTRE = svg.get_centre(DEFAULT['DRAWABLE_AREA'])
bg = set_background(DEFAULT['DRAWABLE_AREA'], "#000")
WORD = "Genuary"
CIRCLE = draw_circle(svg.get_centre(DEFAULT['DRAWABLE_AREA']), 1000, {"fill": "#00f", "clip-path": "url(#clip)"})
noise = objects_to_group(
    list(pixel_noise(MIN_XY, (WIDTH, HEIGHT), 50, True)), "noise", {"clip-path": "url(#clip)"})
text = svg_text(WORD, CENTRE, FONT_STYLES)
clippath = object_to_clip_path(text, "clip")


svg_list.append(bg)
svg_list.append(noise)
svg_list.append(clippath)
# svg_list.append(text)
# svg_list.append(CIRCLE)

doc = svg.build_svg_file(
    DEFAULT['PAPER_SIZE'], DEFAULT['DRAWABLE_AREA'], svg_list)
svg.write_file(DEFAULT['FILENAME'], doc)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Genuary 2024 - Day 7: "Progress Bar"
"""
import time
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
STYLE_LIST = ['black', 0.5, 'gray', 1]
OUTER_BLEED = 100  # px
INNER_BLEED = OUTER_BLEED * 2
PROGRESS = 0.3  # 30%
FIDELITY = 1

# LOCAL FUNCTIONS


def draw_rounded_rectangle(xy_pos, width, height, radius, style_list):
    """
    Returns an SVG rect element as a string with the specified center
    coordinates and radius.

    Args:
        xy_pos (tuple): The x and y coordinates of the upper left corner of the
        rectangle.
        width (float): The width of the rectangle.
        height (float): The height of the rectangle.
        radius (float): The radius of the rounded corners.
        style_list (list): A list of style parameters.

    Returns:
        str: an svg rounded rectangle element as a string.
    """
    rect_def = f"<rect x='{xy_pos[0]}' y='{xy_pos[1]}' "
    rect_def += f"width='{width}' height='{height}' "
    rect_def += f"rx='{radius}' ry='{radius}' "
    rect_style = f"stroke='{style_list[0]}' stroke-width='{style_list[1]}' "
    rect_style += f"fill='{style_list[2]}'"
    return rect_def + "\n" + rect_style + '/>\n'


def is_positive_number(s):
    """return True if s is a positive number, False otherwise"""
    try:
        return float(s) > 0
    except ValueError:
        return False


def timer_to_steps(timer, fidelity):
    """return the number of steps to take given a timer and fidelity"""
    return int(timer / fidelity)


# prompt user to input a number if one not passed when calling the script.


TIMER = input("Timer in seconds: ")
if TIMER is not None or is_positive_number(TIMER):
    print(f"Timer set to {TIMER} seconds.")
else:
    print("Please enter a positive number.")
    TIMER = input("Timer in seconds: ")
TIMER = float(TIMER)


utils.print_params(DEFAULT)

min_x, min_y, max_x, max_y = DEFAULT['DRAWABLE_AREA']
steps = timer_to_steps(TIMER, FIDELITY)
print(f"seconds: {TIMER} fidelity: {FIDELITY} steps: {steps}")
for step in range(steps+1):
    print(f"Step: {step} of {steps}")
    time.sleep(1 / FIDELITY)
    PROGRESS = step / timer_to_steps(TIMER, FIDELITY)
    svg_list = []
    # fill svg_list with svg objects
    svg_list.append(draw_rounded_rectangle((min_x + OUTER_BLEED,
                                            min_y + OUTER_BLEED),
                                           max_x - min_x - (OUTER_BLEED * 2),
                                           max_y - min_y - (OUTER_BLEED * 2),
                                           100,
                                           STYLE_LIST))
    # draw a third rectangle to represent the progress.
    # width is % of the inner rectangle
    svg_list.append(draw.rectangle((min_x + INNER_BLEED, min_y + INNER_BLEED),
                                   (max_x - min_x - (INNER_BLEED * 2)),
                                   max_y - min_y - (INNER_BLEED * 2),
                                   ['black', 0.5, 'white']))

    # third rectangle to represents progress
    fill = svg.get_random_colour()
    svg_list.append(draw.rectangle((min_x + INNER_BLEED, min_y + INNER_BLEED),
                                   (max_x - min_x
                                       - (INNER_BLEED * 2)) * PROGRESS,
                                   max_y - min_y - (INNER_BLEED * 2),
                                   ['black', 0.5, fill]))

    doc = svg.build_svg_file(
        DEFAULT['PAPER_SIZE'], DEFAULT['DRAWABLE_AREA'], svg_list)
    svg.write_file(DEFAULT['FILENAME'], doc)

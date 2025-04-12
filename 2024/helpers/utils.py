#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=consider-using-f-string
# using f-strings, but still clocks an error :/
"""
    General utility functions
"""
import os
import sys
# import datetime # no longer used here; simple file name generation...
import math
from math import pi, cos, sin
import random
import datetime


def create_dir(dir_path):
    """
    Creates a directory at the specified path if it does not already exist.

    Args:
        dir_path (str): The path of the directory to create.

    Returns:
        None
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path


def generate_filename():
    """Generates a filename for the SVG file based on the name of the script

    Returns:
      str: The filename in the format "<name of script>.svg".
    """
    name = sys.argv[0].split(".py")[0]
    return f"{name}.svg"

def generate_filename_with_date():
    """Generates a filename for the SVG file based on the name of the script

    Returns:
      str: The filename in the format "<name of script>.svg".
    """
    name = sys.argv[0].split(".py")[0]
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")[:-3]
    return f"{name}_{date}.svg"


def print_params(param_dict):
    """print the parameters"""
    # if there is a key called 'NAME' in the param_dict, print it
    if 'TITLE' in param_dict:
        # work out length of name
        title = f"--- {param_dict['TITLE']} "
        # print --- name  +  --- (68 - name_length) times
        print(f"{title}{(68-len(title))*'-'}\n")
        # remove the name from the dict
        param_dict.pop('TITLE')
    else:
        print(f"{68*'-'}\n")
    for key, value in param_dict.items():
        print(f"{key}: {value}")
    print(f"\n{68*'-'}")


# Math functions


def quantize(value, step, strategy="floor"):
    """quantize a value to the nearest step, using the specified strategy
    floor - round down to nearest step
    ceil - round up to nearest step
    round - round to nearest step

    Args:
        value (number): input value to quantize
        step (int): quantize step size
        strategy (str, optional): floor, ceil or round. Defaults to "floor".

    Returns:
        int : quantized value
    """
    value_div_step = value / step

    # if floor, round down to nearest step
    if strategy == "floor":
        ret_val = int(math.floor(value_div_step) * step)
    # if ceil, round up to nearest step
    elif strategy == "ceil":
        ret_val = int(math.ceil(value_div_step) * step)
    # if round, round to nearest step
    elif strategy == "round":
        ret_val = int(round(value_div_step) * step)
    return ret_val


def get_fibonacci_list(length):
    """return a list of fibonacci numbers up to max_value"""
    fibonacci_list = [1, 2]
    while len(fibonacci_list) < length:
        fibonacci_list.append(fibonacci_list[-1] + fibonacci_list[-2])
    return fibonacci_list


def print_pct_complete(iteration, total, last_pct_complete):
    """print the percentage complete"""
    pct_complete = int((iteration / total) * 100)
    if pct_complete > last_pct_complete:
        # use sys.stdout.write to print without newline
        sys.stdout.write(f"\r{pct_complete}% complete")
        sys.stdout.flush()
    return pct_complete


def random_point_on_circle(circle):
    """
    Return a random point on a circle.
    Args:
        circle (tuple): A tuple containing the xy position of the centre of
        the circle and the radius.
    """
    angle = random.uniform(0, 2 * pi)
    radius = circle[1]
    x = circle[0][0] + radius * cos(angle)
    y = circle[0][1] + radius * sin(angle)

    return (x, y)


# Random functions


def weighted_random(weight):
    """Return a random number between 0 and weight"""
    return random.random() * weight


def list_to_string(in_list):
    """_summary_

    Args:
        list (list): list of points
    Returns:
        string: string of points
    """
    return ','.join(map(str, in_list))


def calc_output_size(doc):
    """ sum character counts in doc to get output size """
    length = 0
    for element in doc:
        length += len(element)
    return human_values(length)


def human_values(integer):
    """ return a human readable value """
    bold = "\033[1m"
    red = "\033[91m"
    amber = "\033[93m"
    green = "\033[92m"
    normal = "\033[0m"
    fs = "File size: "
    formats = [(10000000, f"{bold}{red}{fs}{{:.2f}}M{normal}", 1000000),
               (1000000, f"{bold}{amber}{fs}{{:.2f}}M{normal}", 1000000),
               (1000, f"{bold}{green}{fs}{{:.2f}}k{normal}", 1000),
               (100, f"{bold}{green}{fs}{{}}b{normal}", 1)]

    for threshold, format_str, divisor in formats:
        if integer > threshold:
            outstr = format_str.format(integer / divisor)
            break
    else:
        outstr = str(integer)  # shouldn't get here...

    print(outstr)
    return outstr

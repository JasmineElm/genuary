#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Genuary 2024 - Day 13: "Wobbly function day."
"""
import random
import numpy as np
from math import sin
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

import toml

# local libraries
from helpers import svg, utils

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
STEPS = 100

# LOCAL FUNCTIONS

x = 1.604
t = 9.36
fib_seq = [1, 2, 3, 5]


def one_range_to_another(item, in_min, in_max, out_min, out_max):
    return (item - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def stack_sines(steps, x, num_list):
    points = []
    for i in range(steps):
        sin1 = sin(x * random.random()*random.choice(num_list) +
                   random.random()*random.choice(num_list) + i
                   * random.random()*random.choice(num_list))
        sin2 = sin(x * random.random()*random.choice(num_list)
                   * random.random()*random.choice(num_list) +
                   random.random()*random.choice(num_list) + i
                   * random.random()*random.choice(num_list))
        sin3 = sin(x * random.choice(num_list) +
                   random.random()*random.choice(num_list) + i
                   * random.random()*random.choice(num_list))
        sin4 = sin(x * random.random()*random.choice(num_list) +
                   random.random()*random.choice(num_list) + i
                   * random.random()*random.choice(num_list))
        ret_sine = sin1 * sin2 + sin3 * sin4
        points.append(ret_sine)
        x += 0.1
    points = [one_range_to_another(
        p, min(points), max(points), 0, 1) for p in points]
    return points


def smooth_points(points):
    # interpolate points to smooth them
    cubic_interpolation_model = interp1d(
        range(len(points)), points, kind='cubic')
    interp_x = np.linspace(0, len(points)-1, 100)
    y = cubic_interpolation_model(interp_x)
    return y


utils.print_params(DEFAULT)

pnts_list = []
for line in range(1, 10, 1):
    # create a noisy copy of pnts
    pnts = stack_sines(STEPS, x, fib_seq)
    # add line to each pnt
    pnts = [pnt + line for pnt in pnts]
    pnts = smooth_points(pnts)
    pnts_list.append(pnts)


# sit fig and axes
fig, ax = plt.subplots(nrows=1, ncols=1)

for pnts in pnts_list:
    plt.plot(pnts, color='white')
# just plot lines, no fill
plt.fill_between(range(len(pnts)), pnts, color='none')
# change line colour to white
# remove axes
ax = plt.gca()
# change background colour
ax.set_facecolor('black')
# remove axes
ax.axes.xaxis.set_visible(False)
ax.axes.yaxis.set_visible(False)


# save svg file
plt.savefig(DEFAULT['FILENAME'], format="svg")

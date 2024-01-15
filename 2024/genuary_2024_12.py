#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Genuary 2024 - Day 12: "Lava lamp."
"""
# import random
import numpy as np
import matplotlib.pyplot as plt
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
    DEFAULT['OUTPUT_DIR']) + '12.svg'})

# LOCAL VARIABLES
height = DEFAULT['DRAWABLE_AREA'][3] - DEFAULT['DRAWABLE_AREA'][1]
width = DEFAULT['DRAWABLE_AREA'][2] - DEFAULT['DRAWABLE_AREA'][0]
ymax, xmax = 3.5, 5

# LOCAL FUNCTIONS

utils.print_params(DEFAULT)


y, x = np.ogrid[ymax:-ymax:height*1j, -xmax:xmax:width*1j]
cy, cx = np.cos(np.cos(y**2)), np.sin(np.sin(x**2))

# plot it
plt.figure(figsize=(100, 150),
           dpi=DEFAULT['PPMM'],
           facecolor='black')

# line thickness for plot = 10px

# plt.imshow(cy - cx, cmap='hot', interpolation='bicubic')
plt.axis('off')
plt.contour(x.ravel(), y.ravel(), (cy - cx),  linewidths=10)
# minimise margins
plt.tight_layout(pad=0)

# change background colour

# save svg file
plt.savefig(DEFAULT['FILENAME'], format="svg")

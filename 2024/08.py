#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Genuary day 8 - "Chaotic System"
    borrowed heavily from
    https://resteche.github.io/REsteche_blog/chaos%20theory/butterfly%20effect/python%20animation/2021/10/20/Lorenz_animation.html
"""
import toml
import numpy as np
import matplotlib.pyplot as plt
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

STEPS = 10000
DT = 0.01
DPI = 300
PNG_DPI = DPI / 3
CM_PER_INCH = 2.54

# LOCAL FUNCTIONS


def lorenz(x, y, z, sigma=10, rho=28, beta=2.667):
    """
    Computes the next position in a Lorenz Attractor.

    The Lorenz Attractor is a set of chaotic solutions to the Lorenz system,
    which is a system of ordinary differential equations.

    Parameters:
    x (float): The current x position.
    y (float): The current y position.
    z (float): The current z position.
    sigma (float, optional): The sigma parameter for the Lorenz system.
    rho (float, optional): The rho parameter for the Lorenz system.
    beta (float, optional): The beta parameter for the Lorenz system.

    Returns:
    tuple: The next position (x, y, z) in the Lorenz Attractor.
    """
    x_pos = sigma*(y - x)
    y_pos = rho*x - y - x*z
    z_pos = x*y - beta*z
    return x_pos, y_pos, z_pos


utils.print_params(DEFAULT)


xs = np.empty(STEPS + 1)
ys = np.empty(STEPS + 1)
zs = np.empty(STEPS + 1)


xs[0], ys[0], zs[0] = (0., 1., 1.05)

for i in range(STEPS):
    x_dot, y_dot, z_dot = lorenz(xs[i], ys[i], zs[i])
    xs[i + 1] = xs[i] + (x_dot * DT)
    ys[i + 1] = ys[i] + (y_dot * DT)
    zs[i + 1] = zs[i] + (z_dot * DT)

ax = plt.figure().add_subplot()

ax.plot(xs, zs, c='k', lw=10)
# don't show axes
ax.set_axis_off()


plt.gcf().set_size_inches(DEFAULT['SIZE'][0] / CM_PER_INCH,
                          DEFAULT['SIZE'][1] / CM_PER_INCH)
# set DPI to 300
plt.gcf().set_dpi(DPI)

plt.savefig(DEFAULT['FILENAME'])
# halve the size and save again as png with 1/3 DPI
plt.gcf().set_size_inches(DEFAULT['SIZE'][0] / (CM_PER_INCH*2),
                          DEFAULT['SIZE'][1] / (CM_PER_INCH*2))
plt.savefig(DEFAULT['FILENAME'] + '.png', dpi=DPI / 3)

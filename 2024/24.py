#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    genuary 2024 day 24: Impossible objects (undecided geometry)
"""
from matplotlib.tri import Triangulation
import matplotlib.pyplot as plt
import toml
import numpy as np

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


fig = plt.figure(figsize=(4, 4))
ax = plt.axes(projection='3d')
# don't show the axes
ax.set_axis_off()
# defining parameters
theta = np.linspace(0, 32 * np.pi)
w = np.linspace(-0.5, 0.5, 32)
w, theta = np.meshgrid(w, theta)
phi = 0.5 * theta
# radius in x-y plane
r = 0.5 + w * np.cos(phi)
x = np.ravel(r * np.cos(theta))
y = np.ravel(r * np.sin(theta))
z = np.ravel(w * np.sin(phi))
tri = Triangulation(np.ravel(w), np.ravel(theta))
# rotate the axes by 90 degrees, update the viewing limits
# ax.view_init(45, 45, 90)
ax.plot_trisurf(x, y, z, triangles=tri.triangles, linewidths=0.5,
                edgecolor='black', color='white', shade=False)
# minimize the margins
plt.tight_layout()

# save the plot as svg
plt.savefig(DEFAULT['FILENAME'], bbox_inches='tight')
plt.show()

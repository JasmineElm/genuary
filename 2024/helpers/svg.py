#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    SVG functions
"""
import math
import random


def set_image_size(paper_size, ppmm, landscape=True):
    """Set the size of the image in pixels.

    Args:
        paper_size (tuple): (width, height)
        ppmm (int): (pixels per mm)
        landscape (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
    """
    out_size = (int(paper_size[0] * ppmm), int(paper_size[1] * ppmm))
    return set_landscape(out_size, landscape)


def set_landscape(paper_size, landscape):
    """rotates a paper size tuple if landscape is True

    Args:
        paper_size (tuple): (width, height)
        landscape (bool): True if landscape

    Returns:
        tuple: (width, height)
    """
    if landscape:
        paper_size = (paper_size[1], paper_size[0])
    return paper_size


def set_drawable_area(paper_size, bleed_xy):
    """ returns a tuple of the drawable area defined by the bleed

    Args:
        paper_size (tuple): (width, height)
        bleed_xy (int): percentage of bleed

    Returns:
        tuple: (min_x, min_y, width, height)
    """
    min_x = int((paper_size[0] * bleed_xy[0] / 100)/2)
    min_y = int((paper_size[1] * bleed_xy[1] / 100)/2)
    width = paper_size[0] - (min_x * 2)
    height = paper_size[1] - (min_y * 2)
    return (min_x, min_y, width, height)


def viewbox_to_drawable_area(viewbox):
    """Convert viewbox to x,y coordinates"""
    x1, y1, width, height = viewbox
    x2 = x1 + width
    y2 = y1 + height
    return x1, y1, x2, y2


def is_in_drawable_area(xy1, xy2, viewbox):
    """ return True if both points are in drawable_area """
    drawable_area = viewbox_to_drawable_area(viewbox)
    return (drawable_area[0] <= xy1[0] <= drawable_area[2] and
            drawable_area[1] <= xy1[1] <= drawable_area[3] and
            drawable_area[0] <= xy2[0] <= drawable_area[2] and
            drawable_area[1] <= xy2[1] <= drawable_area[3])

# Circles


def calculate_max_radius(drawable_area):
    """
    Calculates the maximum radius that can be used for concentric circles on a
    canvas of the given size.

    Args:
      drawable_area (tuple): the width and height of the
      canvas.

    Returns:
      int: The maximum radius that can be used for concentric circles on the
      canvas.
    """
    return min(drawable_area[3] - drawable_area[1],
               drawable_area[2] - drawable_area[0]) * 0.5


def set_circle(drawable_area, size=0.95):
    """ set the xy, radius for the largest circle that fits in drawable_area
        circle will be centred on both axes, and be 95% of the smallest
        drawable_area dimension
    """
    pos_x = (drawable_area[0] + drawable_area[2]) / 2
    pos_y = (drawable_area[1] + drawable_area[3]) / 2
    pos_xy = [pos_x, pos_y]
    radius = calculate_max_radius(drawable_area) * size
    return (pos_xy, radius)

# Header and footer


def svg_header(paper_size, drawable_area):
    """
    Returns an SVG header string with the specified paper and canvas sizes.

    Args:
        paper_size (tuple): the width and height of the paper.
        canvas_size (tuple): the width and height of the canvas.

    Returns:
        str: An SVG header string with the specified paper and canvas sizes.
    """
    xml1 = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>\n"
    xml1 += f"<svg width='{paper_size[0]}' height='{paper_size[1]}' "
    xml1 += f"viewBox='{drawable_area[0]} {drawable_area[1]} "
    xml1 += f"{drawable_area[2]} {drawable_area[3]}' "
    xml1 += "xmlns='http://www.w3.org/2000/svg' version='1.1'>"
    return xml1


def svg_footer():
    """return the SVG footer"""
    return "</svg>"

# build SVG file


def svg_list_to_string(svg_list):
    """ convert a list of SVG lines to a string """
    return "\n".join(svg_list)


def build_svg_file(paper_size, drawable_area, svg_list):
    """ build the SVG file from the following parts:
        header
        svg_list
        footer
    """
    svg_list.insert(0, svg_header(paper_size, drawable_area))
    svg_list.append(svg_footer())
    return svg_list


def write_file(filename, svg_list):
    """ Write the SVG file """
    with open(filename, "w", encoding="utf-8") as svg_file:
        # make sure svg_list is a list of strings
        if type(svg_list) is None:
            print("svg_list is empty")
            return
        if type(svg_list[0]) is not str:
            print("svg_list is not a list of strings")
            return
        for line in svg_list:
            svg_file.write(line + "\n")


# overlap functions

def circles_intersect(circle_a, circle_b):
    """ return True if circles intersect """
    distance = math.sqrt((circle_a[0] - circle_b[0])**2 +
                         (circle_a[1] - circle_b[1])**2)
    # return True if distance between centres is less than sum of radii
    return distance < circle_a[2] + circle_b[2]


def set_bounding_box(points_list):
    """ return a bounding box for a list of points """
    min_x = min_y = float('inf')
    max_x = max_y = float('-inf')

    for point in points_list:
        x, y = point
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

    return (min_x, min_y, max_x, max_y)


def bounding_box_intersect(box_a, box_b):
    """ return True if bounding boxes overlap """
    if box_a[2] < box_b[0] or box_a[0] > box_b[2] or \
       box_a[3] < box_b[1] or box_a[1] > box_b[3]:
        return False
    return True


# Positioning functions


def get_centrality(viewbox, xy):
    """_summary_

    Args:
        viewbox ([xy1, xy2]): canvas size
        xy ([x,y]): point to check

    Returns:
        float: float between 0 and 1, depending on the distance of
        (x,y) from the centre of the canvas
        0 = centre, 1 = edge
    """
    dx = viewbox[0] - xy[0]
    dy = viewbox[1] - xy[1]
    distance = math.hypot(dx, dy)

    dx_viewbox = viewbox[0] - viewbox[2]
    dy_viewbox = viewbox[1] - viewbox[3]
    max_distance = math.hypot(dx_viewbox, dy_viewbox)

    return distance / max_distance


def get_centre(viewbox):
    """Return the centre of the canvas"""
    diff_x = viewbox[2] - viewbox[0]
    diff_y = viewbox[3] - viewbox[1]
    return (diff_x / 2, diff_y / 2)


def get_random_point(viewbox):
    """Return a random point within the canvas"""
    return (random.randint(viewbox[0], viewbox[2]),
            random.randint(viewbox[1], viewbox[3]))


def set_polygon_size(viewable_area, polygons_per_min_dimension):
    """Set a polygon size based on how many will fit
       in the smallest dimension

    Args:
        viewable_area ([xy1, xy2]): drawable area
        polygons_per_min_dimension (int): how many polygons can fit in the
                                          smallest dimension
    returns:
        int: size of polygon
    """
    smallest_dimension = min(viewable_area[2] - viewable_area[0],
                             viewable_area[3] - viewable_area[1])
    return int(smallest_dimension / polygons_per_min_dimension)


def set_polygon(xy, polygon_size, points):
    """_summary_

    Args:
        xy ([x,y]): xy coordinates of centre of polygon
        polygon_size (int): diameter of polygon
        points (int): number of points that make up the polygon
    Returns:
        list: list of points that make up the polygon
    """
    polygon = []
    for i in range(points):
        # set a point on the circumference
        angle = i * (2 * math.pi / points)
        polygon.append(xy[0] + math.cos(angle) * polygon_size / 2)
        polygon.append(xy[1] + math.sin(angle) * polygon_size / 2)
    return polygon

# Grid functions


def generate_square_grid(canvas, grid_size, noise=0.05):
    """return a list of points that fit within the grid
        grid begins at canvas[0] + grid_size, canvas[1] + grid_size
        grid ends at canvas[2] - grid_size, canvas[3] - grid_size
        noise is a percentage of the grid_size"""
    # store canvas boundaries in variables
    x_start = canvas[0]
    y_start = canvas[1]
    x_end = canvas[2]
    y_end = canvas[3]

    # if noise is 0, use list comprehension
    if noise == 0:
        return [(x, y)
                for x in range(x_start, x_end, grid_size)
                for y in range(y_start, y_end, grid_size)]

    # if noise is not 0, use generator expression
    return ((x + random.uniform(-grid_size * noise, grid_size * noise),
             y + random.uniform(-grid_size * noise, grid_size * noise))
            for x in range(x_start, x_end, grid_size)
            for y in range(y_start, y_end, grid_size))


def get_relationships(start_xy, end_xy, diag_def=3):
    """determine direction between end_xy and start_xy"""
    diff_x = end_xy[0] - start_xy[0]
    diff_y = end_xy[1] - start_xy[1]
    abs_diff_x = abs(diff_x)
    abs_diff_y = abs(diff_y)
    diag_x = diff_x / diag_def
    diag_y = diff_y / diag_def
    mode = ""
    # if diff_x > diff_y and diff Y < 1/3 diff_x, hotioontal
    if abs_diff_x > abs_diff_y and abs_diff_y < abs(diag_x):
        mode = "horizontal"
    # if diff_y > diff_x and diff_x < 1/3 diff_y, vertical
    if abs_diff_y > abs_diff_x and abs_diff_x < abs(diag_y):
        mode = "vertical"
    if diff_x > 0:
        if diff_y > 0:
            mode = "diagonal_down"
        else:
            mode = "diagonal_up"
    return mode


def join_points(point, neighbours, direction, sparseness=0.5, diag_def=3):
    """return tuples of [start, end] points for each neighbour
    direction sets the direction of the line; horizontal, vertical, diagonal
    sparseness is whether to return all points or a subset"""
    # filter neighbours by direction
    neighbours = [n for n in neighbours
                  if get_relationships(point, n, diag_def) == direction]
    # filter this list by sparseness
    neighbours = [n for n in neighbours if random.random() > sparseness]
    # return a list of tuples of [start, end] points
    return [[point, n] for n in neighbours]


def get_neighbours(point, grid, radius):
    """return a list of points within radius of point"""
    return [p for p in grid if (point[0] - radius <= p[0] <= point[0] + radius
                                and point[1] - radius <=
                                p[1] <= point[1] + radius)]


def get_random_colour():
    """Return a random hex colour string."""
    hex_colour = "#"+hex(random.randint(0, 16777215))[2:]
    return hex_colour


def get_random_coordinates(canvas):
    """get random coordinates within the canvas

    Args:
        canvas (tuple): [min_x, min_y, max_x, max_y]
    """
    x = random.randint(canvas[0], canvas[2])
    y = random.randint(canvas[1], canvas[3])
    return (x, y)

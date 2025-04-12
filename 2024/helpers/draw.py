"""
    This module contains functions used in the body of svg files
"""

# TODO: Jan 10th 2024: draw functions should accept a dict of tags and values
#                      for styling etc., see svg.dict_to_tags() for a starter.

from helpers import svg


def line(start_xy, end_xy, addnl_styles):
    """return a line from start_xy to end_xy"""
    styles = svg.dict_to_tags(addnl_styles)
    linedef = f"<line x1='{start_xy[0]}' y1='{start_xy[1]}' "
    linedef += f" x2='{end_xy[0]}' y2='{end_xy[1]}' {styles} />"
    return linedef


def box(start_xy, box_size, styles):
    """draw a box"""
    position = f" x='{start_xy[0]}' y='{start_xy[1]}' "
    size = f" width='{box_size}' height='{box_size}' "
    stroke = f" stroke='{styles[0]}' stroke-width='{styles[1]}' "
    fill = f" fill='{styles[2]}' "
    return f"<rect {position}{size}{stroke}{fill}/>"


def box2(start_xy, box_size, addnl):
    """draw a box"""
    tags = svg.dict_to_tags(addnl)
    position = f" x='{start_xy[0]}' y='{start_xy[1]}' "
    size = f" width='{box_size}' height='{box_size}' "
    return f"<rect {position}{size}{tags}/>"


def rectangle(start_xy, width, height, styles):
    """draw a box"""
    position = f" x='{start_xy[0]}' y='{start_xy[1]}' "
    size = f" width='{width}' height='{height}' "
    stroke = f" stroke='{styles[0]}' stroke-width='{styles[1]}' "
    fill = f" fill='{styles[2]}' "
    return f"<rect {position}{size}{stroke}{fill}/>"


def circle(xy_pos, radius, style_list, opacity=1, addnl=""):
    """
    Returns an SVG circle element as a string with the specified center
    coordinates and radius.

    Args:
        cx (float): The x-coordinate of the center of the circle.
        cy (float): The y-coordinate of the center of the circle.
        r (float): The radius of the circle.

    Returns:
        str: An SVG circle element as a string.
    """
    circle_def = f"<circle cx='{xy_pos[0]}' cy='{xy_pos[1]}' r='{radius}' "
    circle_style = f"stroke='{style_list[0]}' stroke-width='{style_list[1]}' "
    circle_style += f"fill='{style_list[2]}'"
    circle_style += f" opacity='{opacity}' {addnl} />"
    return circle_def + circle_style + "\n"


def circle2(xy_pos, radius, addnl):
    tags = svg.dict_to_tags(addnl)
    circle_def = f"<circle cx='{xy_pos[0]}' cy='{xy_pos[1]}' r='{radius}' "
    circle_def += f" {tags} />"
    return circle_def


def set_background(drawable_area, background_colour):
    """
    returns a rectangle of background_colour the size of the drawable area
    """
    return box(drawable_area[:2],
               drawable_area[2] - drawable_area[0],
               (background_colour,
               0,
               background_colour))


def quadratic_curve(start_xy, control_xy, end_xy, style_list):
    """return a quadratic curve"""
    start = f"<path d='M {start_xy[0]} {start_xy[1]} "
    control = f"Q {control_xy[0]} {control_xy[1]} "
    end = f"{end_xy[0]} {end_xy[1]}' "
    style = (
        f"stroke='{style_list[0]}' "
        f"stroke-width='{style_list[1]}' "
        f"fill='{style_list[2]}' />"
    )
    return start + control + end + style + "\n"


def polygon(points, style_list):
    """builds a polygon using a string of points
        and a list of styles.

    Args:
        points (string): list of points that make up the polygon
        style_list ([stroke, stroke-width, fill]): styles for the polygon
    Returns:
        svg: svg object
    """
    # draw the polygon
    xml = f"<polygon points='{points}' "
    xml += f"stroke='{style_list[0]}' stroke-width='{style_list[1]}' "
    xml += f"fill='{style_list[2]}' />"
    return xml


def path(coords, style=('black', '1', 'none')):
    """
    Generates an SVG path element from a list of coordinates and a style tuple.

    Parameters:
    coords (list of tuples): A list of (x, y) tuples representing coordinates.
    style (tuple, optional): stroke color, stroke width, and fill color.
                             Defaults to ('black', '1', 'none').

    Returns:
    str: An SVG path element as a string.
    """
    draw_path = " ".join(f"{x} {y} L " for x, y in coords)
    styles = f"stroke='{style[0]}' stroke-width='{style[1]}' fill='{style[2]}'"
    draw_path = f"<path d='M {draw_path}' {styles}/>"
    return draw_path

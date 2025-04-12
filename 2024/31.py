#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Skeleton file for new scripts
"""
import random
import datetime
import toml

# local libraries
from helpers import svg, utils, lsys, draw

# Load config file and set DEFAULT parameters
config = toml.load("config.toml")
DEFAULT = config["DEFAULT"]
# add a title to the DEFAULT dict
DEFAULT.update({"PAPER_SIZE": svg.set_image_size(DEFAULT['SIZE'],
                                                 DEFAULT['PPMM'],
                                                 DEFAULT['LANDSCAPE'])})
DEFAULT.update({"DRAWABLE_AREA": svg.set_drawable_area(DEFAULT['PAPER_SIZE'],
                                                       DEFAULT['BLEED'])})
DEFAULT.update({"FILENAME": utils.create_dir(
    DEFAULT['OUTPUT_DIR']) + utils.generate_filename_with_date()})


def validate_rule_string(rule_string):

    rule_string = rule_string.replace(
        "[]", "").replace("+-", "").replace("-+", "")
    # remove unmatched brackets
    return rule_string


def create_rule_dict(axiom, length):
    directives = ["F", "+", "-", "[", "]"]
    # extend directives to include axiom if not already present
    for char in axiom:
        if char not in directives:
            directives.append(char)
    rules = {}
    for char in axiom:
        rules[char] = ""
        stack = []
        for _ in range(length):
            character = random.choice(directives)
            if character == "[":
                stack.append(character)
            if character == "]":
                if stack:
                    stack.pop()
                else:
                    character = ""
            rules[char] += character
        # remove unmatched brackets
        while stack:
            rules[char] = rules[char].rpartition('[')[0]
            stack.pop()
        rules[char] = validate_rule_string(rules[char])
    return rules


def explain_rules(rules):
    directives = {"F": "draw", "+": "turn left",
                  "-": "turn right", "[": "save position",
                  "]": "restore position"}
    if len(rules) > 1:
        for key in rules:
            for char in rules[key]:
                if char not in directives:
                    rules[key] = rules[key].replace(char, rules[char])
    explanation = ""
    for key in rules:
        # build the directives string
        explanation += f"{key} -> {rules[key]} \n" + \
            "\n".join([directives[char] for char in rules[key]]) + "\n"
        return explanation


def expand_rules(rules):
    directives = ["F", "+", "-", "[", "]"]
    for key in rules:
        for char in rules[key]:
            if char not in directives:
                rules[key] = rules[key].replace(char, rules[char])
    return rules


def set_axiom(length):
    axiom = "F"
    length = random.randint(1, length)
    letters = "xyzabcde"
    length = random.randint(1, length)
    if length > 1:
        axiom += letters[:length]
    return axiom


def set_page_size(object_list):
    """set the page size based a list of xy tuples"""
    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0
    for obj in object_list:
        if obj[0][0] > max_x:
            max_x = obj[0][0]
        if obj[0][1] > max_y:
            max_y = obj[0][1]
        if obj[0][0] < min_x:
            min_x = obj[0][0]
        if obj[0][1] < min_y:
            min_y = obj[0][1]
        if obj[1][0] > max_x:
            max_x = obj[1][0]
        if obj[1][1] > max_y:
            max_y = obj[1][1]
        if obj[1][0] < min_x:
            min_x = obj[1][0]
        if obj[1][1] < min_y:
            min_y = obj[1][1]
    page_size = ((max_x - min_x)//1,
                 (max_y - min_y)//1)
    return page_size


def set_viewbox(object_list):
    """set the viewbox based a list of xy tuples"""
    # if  object list is empty, break
    if not object_list:
        print("Object list is empty")
        exit()
    xs = [coord[0] for obj in object_list for coord in obj]
    ys = [coord[1] for obj in object_list for coord in obj]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    viewbox = (min_x//1, min_y//1, (1 + max_x - min_x) //
               1, (1 + max_y - min_y)//1)
    return viewbox


def set_svg_comment(comment_dict):
    """add a comment to the SVG file"""
    comment_string = "<!--\n"
    for key, value in comment_dict.items():
        if key == "RULES":
            value = str(value)
            value = value.replace("--", "- -").replace("--", "+ - -")
        comment_string += f"{key}: {value}\n"
    comment_string += "-->"
    return comment_string


def date_string():
    """return the current date as a string"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# # LOCAL VARIABLES
LINE_LENGTH = 150
ANGLE_DIVS = list(range(3, 16))

AXIOM = set_axiom(4)
RULES = create_rule_dict(AXIOM, 15)

PARAM_DICT = {"TITLE": "LSYS PARAMS", "N": 6, "AXIOM": AXIOM,
              "RULES": RULES,
              "INITIAL_ANGLE": 360/random.choice(ANGLE_DIVS)*random.choice(ANGLE_DIVS),
              "ROTATE_ANGLE": 360/random.choice(ANGLE_DIVS)*random.choice(ANGLE_DIVS),
              "LINE_LENGTH": LINE_LENGTH,
              "START_POS": (0, 0),
              "CREATED": date_string()}
utils.print_params(PARAM_DICT)


LINE_STYLE = {'stroke': '#fff', 'stroke-width': 10, "stroke-linecap": "round"}
# LOCAL FUNCTIONS


svg_list = []

tree = lsys.set_lsys_string(
    PARAM_DICT["AXIOM"], PARAM_DICT["RULES"], PARAM_DICT["N"])
print(tree)
lines = lsys.lsys_to_lines(
    tree, PARAM_DICT["START_POS"],
    PARAM_DICT["INITIAL_ANGLE"],
    PARAM_DICT["LINE_LENGTH"],
    PARAM_DICT["ROTATE_ANGLE"])
DEFAULT['PAPER_SIZE'] = set_page_size(lines)

DEFAULT['DRAWABLE_AREA'] = set_viewbox(lines)
svg_list.append(set_svg_comment(PARAM_DICT))
utils.print_params(DEFAULT)
if len(lines) < 5:
    # less than 5 lines, we should break
    print("Not enough lines to draw")
    exit()
# remove any duplicate lines
lines = list(set(lines))
for line in lines:
    svg_list.append(draw.line(line[0], line[1], DEFAULT['LINE_STYLE']))
# fill svg_list with svg objects

doc = svg.build_svg_file(DEFAULT['PAPER_SIZE'],
                         DEFAULT['DRAWABLE_AREA'],
                         svg_list)


svg.write_file(DEFAULT['FILENAME'], doc)

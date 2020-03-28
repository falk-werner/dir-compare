#!/usr/bin/env python3

import sys
import json
import argparse
import math
import xml.etree.ElementTree as ET

from collections import namedtuple

Point = namedtuple('Point', 'x y')
max_level = 0

def get_class_property(class_name, property_name):
    classes = {
        'unchanged': {'fill': 'grey' , 'stroke': 'black'},
        'removed'  : {'fill': 'red'  , 'stroke': 'black'},
        'added'    : {'fill': 'green', 'stroke': 'black'},
        'modified' : {'fill': 'blue' , 'stroke': 'black'},
    }
    default_values = {'fill': 'none', 'stoke': 'black'}
    if class_name in classes:
        return classes[class_name][property_name]
    else:
        return default_values[property_name]

def get_point(radius, i):
    angle = (2 * math.pi / 100) * i
    x =  radius * math.sin(angle)
    y = -radius * math.cos(angle)
    return Point(x, y)

def add_segment(label, inner_radius, outer_radius, start, end, class_name=''):
    p1 = get_point(inner_radius, start)
    p2 = get_point(outer_radius, start)
    p3 = get_point(outer_radius, end)
    p4 = get_point(inner_radius, end)
    flip = 0 if math.fabs(end - start) < 50 else 1
    d = ' '.join(str(item) for item in [
        'M', p1.x, p1.y,
        'L', p2.x, p2.y,
        'A', outer_radius, outer_radius, 0, flip, 1, p3.x, p3.y,
        'L', p4.x, p4.y,
        'A', inner_radius, inner_radius, 0, flip, 0, p1.x, p1.y,
        'z'])

    fill = get_class_property(class_name, 'fill')
    stroke = get_class_property(class_name, 'stroke')
    ET.SubElement(svg, 'path', {'d' : d, 'data-label': label, 'class': class_name, 'fill': fill, 'stroke': stroke})

def walk(svg, node, inner_radius=100, start=0, end=100, path='', level=1):
    global max_level
    if level > max_level:
        max_level = level
    outer_radius = inner_radius + 50
    width = end - start
    for child in node['children']:
        child_width = (child['weight'] * width) / (node['weight'])
        child_end = start + child_width
        child_name = child['name']
        child_path = path + "/" + child_name
        add_segment(child_path, inner_radius, outer_radius, start, child_end, child['class'])
        walk(svg, child, outer_radius, start, child_end, child_path, level + 1)
        start = child_end

parser = argparse.ArgumentParser(description='Generates a Sunburst diagram from a tree')
parser.add_argument('-i', '--input', type=str, required=False, default=None, help='Path of input file (default: used stdin)')
args = parser.parse_args()

if args.input is None:
    source = json.load(sys.stdin)
else:
    with open(args.input) as input_file:
        source = json.load(input_file)

svg = ET.Element('svg')
ET.SubElement(svg, 'title').text = 'Sunburst'
ET.SubElement(svg, 'desc').text = 'Sunburst'

walk(svg, source, 50)

size = 50 + (50 * max_level) + 10
svg.set('viewBox', '%d %d %d %d' % (-size, -size, 2 * size, 2 * size))
svg.set('xmlns', 'http://www.w3.org/2000/svg')
svg.set('version', '1.1')


tree = ET.ElementTree(svg)
tree.write(sys.stdout, xml_declaration=True, encoding='unicode')
print()

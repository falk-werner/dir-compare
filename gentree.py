#!/usr/bin/env python3

import json
import os
import sys
import argparse

class Node:
    def __init__(self, name, class_name=''):
        self.name = name
        self.weight = 0
        self.children = []
        self.class_name = class_name
    
    def add(self, path):
        if len(path) > 0:
            self.weight += 1
            child_name = path.pop(0)
            child = next((node for node in self.children if node.name == child_name), None)
            if child is None:
                child = Node(child_name, self.class_name)
                self.children.append(child)
                if len(path) is 0:
                    child.weight = 1
            child.add(path)

    def add_node(self, node):
        self.weight += node.weight
        self.children.append(node)
                

class NodeEncoder(json.JSONEncoder):
    def default(self, obj):
            if (isinstance(obj, Node)):
                return { 'name': obj.name, 'class': obj.class_name, 'weight': obj.weight, 'children': obj.children }
            else:
                return json.JSONEncoder.default(self, obj)

def add_files(root, name, files):
    node = Node(name, name)
    for file_name in files:
        path = file_name.split(os.path.sep)
        node.add(path)
    root.add_node(node)

parser = argparse.ArgumentParser(description='Converts json output from dircmp into a tree')
parser.add_argument('-i', '--input', type=str, required=False, default=None  , help='path of input file (if not specified, stdin is used)')
parser.add_argument('-n', '--name' , type=str, required=False, default='root', help='name of root node (default: root)')
parser.add_argument('-p', '--pretty', action='store_true', help='pretty print json output')
args = parser.parse_args()

if args.input is None:
    source = json.load(sys.stdin)
else:
    with open(args.input) as input_file:
        source = json.load(input_file)

root = Node(args.name)
add_files(root, 'unchanged', source['unchanged'])
add_files(root, 'removed'  , source['removed'])
add_files(root, 'added'    , source['added'])
add_files(root, 'modified' , source['modified'])

if args.pretty:
    print(json.dumps(root, indent=4, cls=NodeEncoder))
else:
    print(json.dumps(root, cls=NodeEncoder))

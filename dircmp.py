#!/usr/bin/env python3

import os
import filecmp
import json
import argparse

def dircmp(left, right):
    removed = set()
    modified = set()
    unchanged = set()
    added = set()
    for root, _, files in os.walk(left):
        for name in files:
                relative_filename = os.path.relpath(os.path.join(root, name), left)
                removed.add(relative_filename)
    for root, _, files in os.walk(right):
        for name in files:
                right_file = os.path.join(root, name)
                relative_filename = os.path.relpath(right_file, right)
                if relative_filename in removed:
                    removed.discard(relative_filename)
                    left_file = os.path.join(left, relative_filename)
                    if (filecmp.cmp(left_file, right_file, False)):
                        unchanged.add(relative_filename)
                    else:
                        modified.add(relative_filename)
                else:
                    added.add(relative_filename)
    return { 'removed': list(removed), 'modified': list(modified), 'unchanged': list(unchanged), 'added': list(added) }

parser = argparse.ArgumentParser(description='Compares two directories.')
parser.add_argument('-l', '--left', required=True, type=str, help='initial directory')
parser.add_argument('-r', '--right', required=True, type=str, help='changed directory')
parser.add_argument('-f', '--format', required=False, type=str, default='text', help='output format: text json')
parser.add_argument('-b', '--brief', action='store_true', help="print summy only (text ouput only)")
parser.add_argument('-u', '--skip-sort', action='store_true', help="print files unsorted (text ouput only)")
args = parser.parse_args()

result = dircmp(args.left,args.right)
if 'json' == args.format:
    print(json.dumps(result))
else:
    print("# compare %s vs. %s" % (args.left, args.right))
    print('#')
    print("# unchanged files: %d" % len(result['unchanged']))
    print("# removed   files: %d" % len(result['removed']))
    print("# added     files: %d" % len(result['added']))
    print("# changed   files: %d" % len(result['modified']))
    print('#')
    print("# total     files: %d" % ( len(result['unchanged']) + len(result['removed']) + len(result['added']) + len(result['modified']) ))

    if not args.brief:
        if not args.skip_sort:
            result['unchanged'].sort()
            result['removed'].sort()
            result['added'].sort()
            result['modified'].sort()
    
        print()
        for name in result['unchanged']:
                print("U %s" % name)
        for name in result['removed']:
                print("D %s" % name)
        for name in result['added']:
                print("A %s" % name)
        for name in result['modified']:
                print("M %s" % name)

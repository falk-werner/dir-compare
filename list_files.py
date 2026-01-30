#!/usr/bin/env python3

import argparse
import os

def sort_key(entry):
    return -entry[1]

def get_files(dirname: str):
    results = dict()
    for (root, _, files) in os.walk(dirname, followlinks=False):
        for filename in files:
            path = os.path.join(root, filename)
            relpath = os.path.relpath(path, dirname)
            if os.path.isfile(path) and not os.path.islink(path):
                size = os.path.getsize(path)
                results[relpath] = size
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("base", type=str)
    parser.add_argument("other", type=str)
    args = parser.parse_args()
    base_files = get_files(args.base)
    other_files = get_files(args.other)

    # Common Files
    files = []
    growth = 0
    for (base_name, base_size) in base_files.items():
        if base_name in  other_files:
            other_size = other_files[base_name]
            files.append( (base_name, other_size - base_size) )
            growth += other_size - base_size
    files.sort(key=sort_key)
    common_count = len(files)
    common_size = growth
    print(f"Common Files: count={len(files)}, size={growth}")
    for (name, size) in files:
        print(f"  {name}: {size}")
    print()

    # Removed Files
    files = []
    growth = 0
    for (base_name, base_size) in base_files.items():
        if not base_name in  other_files:
            files.append( (base_name, base_size) )
            growth += base_size
    files.sort(key=sort_key)
    removed_count = len(files)
    removed_size = growth
    print(f"Removed Files: count={len(files)}, size={growth}")
    for (name, size) in files:
        print(f"  {name}: {size}")
    print()

    # New Files
    files = []
    growth = 0
    for (other_name, other_size) in other_files.items():
        if not other_name in  base_files:
            files.append( (other_name, other_size) )
            growth += other_size
    files.sort(key=sort_key)
    new_count = len(files)
    new_size = growth
    print(f"New Files: count={len(files)}, size={growth}")
    for (name, size) in files:
        print(f"  {name}: {size}")
    print()

    print(f"Changed: count={common_count}, size={common_size}")
    print(f"Removed: count={removed_count}, size={removed_size}")
    print(f"New    : count={new_count}, size={new_size}")
    print(f"Delta  : count={new_count - removed_count}, size={common_size - removed_size + new_size}")


if __name__ == '__main__':
    main()

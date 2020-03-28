#!/bin/bash

BASE=/tmp/dir-compare/test

rm -rf "$BASE"

LEFT="$BASE/left"
mkdir -p "$LEFT"
echo removed   > "$LEFT/removed"
echo unchanged > "$LEFT/unchanged"
echo changed   > "$LEFT/changed"
mkdir -p "$LEFT/subdir"
echo removed   > "$LEFT/subdir/removed"
echo unchanged > "$LEFT/subdir/unchanged"
echo changed   > "$LEFT/subdir/changed"
mkdir -p "$LEFT/removed_subir"
echo removed   > "$LEFT/removed_subir/removed"

RIGHT="$BASE/right"
mkdir -p "$RIGHT"
echo added     > "$RIGHT/added"
echo unchanged > "$RIGHT/unchanged"
echo CHANGED   > "$RIGHT/changed"
mkdir -p "$RIGHT/subdir"
echo added     > "$RIGHT/subdir/added"
echo unchanged > "$RIGHT/subdir/unchanged"
echo CHANGED   > "$RIGHT/subdir/changed"
mkdir -p "$RIGHT/added_subir"
echo added     > "$RIGHT/added_subir/added"

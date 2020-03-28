# dir-compare

Compare two directories

## dircmp

The script *dircmp.py* is used to compare two directories called *left* and *right*.
Where *left* is the initial directory and *right* the modified directory.

### Command Line Arguments

| Argument        | Type   | Description                                              |
| --------------- | ------ | -------------------------------------------------------- |
| -l, --left      | string | Path of initial directory (*left*)                       |
| -r, --right     | string | Path of modified directory (*right*)                     |
| -f, --format    | string | Specify output format: text or json (default: text)      |
| -b, --brief     | flag   | If specified, only summary is printed (text output only) |
| -u, --skip-sort | flag   | If specified, output is not sorted (text output only)    |

### Example

    > test/create_test_data.sh
    > ./dircmp.py -l /tmp/dir-compare/test/left -r /tmp/dir-compare/test/right
    # compare /tmp/dir-compare/test/left vs. /tmp/dir-compare/test/right
    #
    # unchanged files: 2
    # removed   files: 3
    # added     files: 3
    # changed   files: 2
    #
    # total     files: 10

    U subdir/unchanged
    U unchanged
    D removed
    D removed_subir/removed
    D subdir/removed
    A added
    A added_subir/added
    A subdir/added
    M changed
    M subdir/changed

## gentree

Takes the json output from *dircmp* and converts it into a tree structure.

### Command Line Arguments

| Argument     | Type   | Description                                                         |
| ------------ | ------ | ------------------------------------------------------------------- |
| -i, --input  | string | Optional. Speficies the path of the input file (default: use stdin) |
| -n, --name   | string | Optional. Name of the root node (default: root)                     |
| -p, --pretty | flag   | If specified, JSON output is pretty printed                         |

### Example

    > test/create_test_data.sh
    > ./dircmp.py -l /tmp/dir-compare/test/left -r /tmp/dir-compare/test/right -f json | ./gentree.py -p
    {
        "name": "root",
        "weight": 15,
        "children": [
            {
                "name": "unchanged",
                "weight": 3,
                "children": [
                    {
                        "name": "subdir",
                        "weight": 2,
                        "children": [
                            {
                                "name": "unchanged",
                                "weight": 1,
                                "children": []
                            }
                        ]
                    },
                    // ...
                ]
            }
        ]
    }

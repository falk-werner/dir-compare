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

## Example

    test/create_test_data.sh
    ./dircmp.py -l /tmp/dir-compare/test/left -r /tmp/dir-compare/test/right

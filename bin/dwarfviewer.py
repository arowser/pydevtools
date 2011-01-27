#!/usr/bin/env python
from sys import argv, path
path.append('..')

from devtools.dwarf import DWARF
from devtools.dwarf.viewer import Viewer


if __name__ == '__main__':
    if len(argv) < 2:
        file_path = "../test/test"
    else:
        file_path = argv[1]
    dwarf = DWARF(file_path)
    Viewer(dwarf)

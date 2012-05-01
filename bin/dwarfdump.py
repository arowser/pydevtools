#!/usr/bin/env python
from sys import argv, path
path.append('..')

from bintools.dwarf import DWARF
from bintools.utils import benchmark


def dwarfdump(file_path):
    dwarf = DWARF(file_path)
    print(dwarf)


if __name__ == '__main__':
    if len(argv) < 2:
        file_path = "../test/test"
    else:
        file_path = argv[1]
    
    benchmark(dwarfdump, file_path)


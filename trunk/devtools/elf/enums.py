"""
Copyright (c) 2010, Cambridge Silicon Radio Ltd.
Written by Emilio Monti <emilmont@gmail.com>
"""
class STT:
    NOTYPE = 0
    OBJECT = 1
    FUNCT = 2
    SECTION = 3
    FILE = 3
    LOPROC = 13
    HIPROC = 15


class STB:
    LOCAL = 0
    GLOBAL = 1
    WEAK = 2
    LOPROC = 13
    HIPROC = 15


class SHT:
    NULL = 0
    PROGBITS = 1
    SYMTAB = 2
    STRTAB = 3
    RELA = 4
    HASH = 5
    DYNAMIC = 6
    NOTE = 7
    NOBITS = 8
    REL = 9
    SHLIB = 10
    DYNSYM = 11
    LOPROC = 0x70000000
    HIPROC = 0x7fffffff
    LOUSER = 0x80000000
    HIUSER = 0xffffffff


class SHF:
    WRITE = 0x1
    ALLOC = 0x2
    EXECINSTR = 0x4
    MASKPROC = 0xf0000000

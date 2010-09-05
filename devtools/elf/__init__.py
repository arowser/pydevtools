"""
Copyright (c) 2010, Cambridge Silicon Radio Ltd.
Written by Emilio Monti <emilmont@gmail.com>
"""
from devtools.elf.stream import ElfFile
from devtools.elf.structs import *


class ELF(ElfFile):
    def __init__(self, path):
        ElfFile.__init__(self, path)
        
        # HEADER
        self.header = Header(self)
        
        # LOAD PROGRAM and SECTION HEADER TABLES
        self.prog_headers = self.load_entries(self.header.ph_offset, self.header.ph_count, ProgramHeader)
        self.sect_headers = self.load_entries(self.header.sh_offset, self.header.sh_count, SectionHeader)
        
        # LOAD SECTION HEADERS STRING TABLE
        strtab = self.sect_headers[self.header.shstrndx]
        self.shstrtab = StringTable(self, strtab.offset, strtab.size)
        
        # Create a section dictionary
        self.sect_dict = {}
        for sec in self.sect_headers:
            self.sect_dict[sec.get_name()] = sec
        
        # LOAD STRING TABLE
        strtab = self.sect_dict['.strtab']
        self.strtab = StringTable(self, strtab.offset, strtab.size)
        
        # LOAD SYMBOL TABLE
        symtab = self.sect_dict['.symtab']
        count = symtab.size / Symbol.LENGTH
        self.symbols = self.load_entries(symtab.offset, count, Symbol)

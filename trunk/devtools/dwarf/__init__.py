"""
Copyright (c) 2010, Cambridge Silicon Radio Ltd.
Written by Emilio Monti <emilmont@gmail.com>
"""
from devtools.elf import ELF
from devtools.elf.structs import StringTable

from devtools.dwarf.stream import DwarfStream
from devtools.dwarf.abbrev import AbbrevLoader
from devtools.dwarf.info import DebugInfoLoader
from devtools.dwarf.line import StatementProgramLoader
from devtools.dwarf.pubnames import PubNamesLoader
from devtools.dwarf.aranges import ARangesLoader
from devtools.dwarf.ranges import RangesLoader
from devtools.dwarf.frame import FrameLoader
from devtools.dwarf.loc import LocationLoader


class DWARF(ELF, DwarfStream):
    def __init__(self, path, addr_size=4):
        ELF.__init__(self, path)
        DwarfStream.__init__(self, addr_size)
        
        # DEBUG STRING TABLE
        debug_str = self.sect_dict['.debug_str']
        self.debug_str = StringTable(self, debug_str.offset, debug_str.size)
        
        # DEBUG LINE
        self.stmt = StatementProgramLoader(self)
        
        # DEBUG ABBREV
        self.abbrev = AbbrevLoader(self)
        
        # DEBUG INFO
        self.info = DebugInfoLoader(self)
        
        # DEBUG PUBNAMES
        self.pubnames = PubNamesLoader(self)
        
        # DEBUG ARANGES
        self.aranges = ARangesLoader(self)
        
        # DEBUG RANGES
        self.ranges = RangesLoader(self)
        
        # DEBUG FRAME
        self.frame = FrameLoader(self)
        
        # DEBUG LOC
        self.loc = LocationLoader(self)
    
    # Lookup by location
    def get_addr_by_loc(self, filename, line):
        cu = self.info.get_cu_by_filename(filename)
        lines = self.stmt.get(cu)
        file_index = lines.get_file_index(filename)
        return lines.get_addr_by_loc(file_index, line)
    
    # Lookup by symbol
    def get_loc_by_sym(self, symname):
        die = self.pubnames.get_die(symname)
        decl_file = die.attr_dict['decl_file'].get_value()
        decl_line = die.attr_dict['decl_line'].value
        return (decl_file, decl_line, 0)
    
    def get_addr_by_sym(self, symname):
        die = self.pubnames.get_die(symname)
        file_index = die.attr_dict['decl_file'].value
        decl_line = die.attr_dict['decl_line'].value
        lines = self.stmt.get(die.cu)
        return lines.get_addr_by_loc(file_index, decl_line)
    
    # Lookup by address
    def get_loc_by_addr(self, addr):
        cu = self.aranges.get_cu_by_addr(addr)
        lines = self.stmt.get(cu)
        return lines.get_loc_by_addr(addr)
    
    def __str__(self):
        return '\n'.join(map(str,
                [self.info, self.pubnames, self.aranges, self.frame, self.loc]))
